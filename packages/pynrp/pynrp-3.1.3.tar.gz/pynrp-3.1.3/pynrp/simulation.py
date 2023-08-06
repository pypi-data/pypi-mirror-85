# ---LICENSE-BEGIN - DO NOT CHANGE OR MOVE THIS HEADER
# This file is part of the Neurorobotics Platform software
# Copyright (C) 2014,2015,2016,2017 Human Brain Project
# https://www.humanbrainproject.eu
#
# The Human Brain Project is a European Commission funded project
# in the frame of the Horizon2020 FET Flagship plan.
# http://ec.europa.eu/programmes/horizon2020/en/h2020-section/fet-flagships
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
# ---LICENSE-END
"""
An interface to launch or control a simulation instance.
"""

# pylint: disable=W0622


from __future__ import print_function

from builtins import str
from builtins import object

import traceback
import os
import http.client
import json
import logging

from six import string_types
from future import standard_library

from pynrp.requests_client import RequestsClient
from pynrp.config import Config

from pynrp.rosbridge_handler import RosBridgeHandlerProcess

try:
    from urllib2 import HTTPError
except ImportError:
    from urllib.error import HTTPError # pylint: disable=F0401

standard_library.install_aliases()


class Simulation(object):
    """
    Provides an interface to launch or control a simulation instance.
    """

    def __init__(self, http_client, config, vc):
        """
        Initialize a simulation interface and default logger.

        :param http_client: A HTTP client.
        :param config: A loaded Virtual Coach config.
        :param vc: The virtual coach instance.
        """
        assert isinstance(config, Config)
        assert isinstance(http_client, RequestsClient)

        self.__http_client = http_client
        self.__config = config
        self.__vc = vc

        self.__server = None
        self.__server_info = None
        self.__sim_info = None
        self.__sim_url = None
        self.__experiment_id = None

        self.__previous_subtask = None

        self.__ros_client = None
        self.__status_callbacks = []

        # class level logger so that we can change the name of the logger dynamically
        # when we have more information for this particular simulation
        self.__logger = logging.getLogger('Simulation')

    # pylint: disable=too-many-locals
    def launch(self, experiment_id, experiment_conf, server, reservation, cloned=True,
               storage_token=None, brain_processes=1, profiler='disabled'):
        """
        Attempt to launch and initialize the given experiment on the given servers. This
        should not be directly invoked by users, use the VirtualCoach interface to validate
        and launch a simulation.

        :param experiment_id: A string representing the short name of the experiment to
                              be launched (e.g. ExDTemplateHusky).
        :param experiment_conf: A string representing the configuration file for the experiment.
        :param server: A string representing the name of the server to try to launch on.
        :param reservation: A string representing a cluster resource reservation (if any).
        :param cloned: Boolean. True if the experiment is cloned.
        :param storage_token: A string representing the token for storage authorization.
        :param brain_processes: Number of mpi processes in the brain simulation.
        :param profiler: profiler option. Possible values are: disabled, cle_step and cprofile.
        """
        assert isinstance(experiment_id, string_types)
        assert isinstance(experiment_conf, string_types)
        assert isinstance(server, string_types)
        assert isinstance(reservation, (string_types, type(None)))

        # do not allow reuse of this instance if a simulation has been launched
        if self.__server:
            raise Exception(
                'Invalid call to launch on already created simulation!')

        # print information about the specific server/reservation
        self.__logger.info('Attempting to launch %s on %s.',
                           experiment_id, server)
        if reservation is not None:
            self.__logger.info('Using supplied reservation: %s', reservation)

        # attempt to launch, if any stage fails then print the reason and fail
        try:

            # get the information for the server - this provides urls for endpoints
            server_info_url = '%s/%s' % (
                self.__config['proxy-services']['server-info'], server)
            _, server_json = self.__http_client.get(server_info_url)
            self.__server_info = json.loads(server_json)

            # attempt to launch the simulation with given parameters on the server
            url = '%s/%s' % (self.__server_info['gzweb']['nrp-services'],
                             self.__config['simulation-services']['create'])
            sim_info = {'experimentID': experiment_id,
                        'brainProcesses': brain_processes,
                        'profiler': profiler,
                        'experimentConfiguration': experiment_conf,
                        'gzserverHost': self.__server_info['serverJobLocation'],
                        'reservation': reservation,
                        'private': cloned}

            status_code, sim_json = self.__http_client.post(url, sim_info)

            # check to see if the launch was successful, any other failure return codes
            # such as 404 will trigger an exception by the OIDCClient itself
            if status_code == http.client.CONFLICT:
                raise Exception(
                    'Simulation server is launching another experiment.')

            if status_code != http.client.CREATED:
                raise Exception(
                    "Simulation responded with HTTP status %s" % status_code)

            # retrieve and store the simulation information
            self.__sim_info = json.loads(sim_json)

            # update the logger with specific simulation information, this is useful if
            # multiple concurrent simulations may be run
            log_info = 'Simulation (%s - %s #%s)' % (experiment_id, server,
                                                     self.__sim_info['simulationID'])
            self.__logger = logging.getLogger(log_info)
            self.__logger.info('Simulation Successfully Created.')

        # pylint: disable=broad-except
        except Exception as e:
            # print any launch failures and return False so the next server can be tried
            self.__logger.error('Unable to launch on %s: %s', server, str(e))
            traceback.print_exc()
            return False

        # store server information, experiment_id and the endpoint url for this server/simulation id
        self.__server = server
        self.__sim_url = '%s/%s' % (url, self.__sim_info['simulationID'])
        self.__experiment_id = experiment_id

        # Connect to rosbridge and create subscribers
        ws_url = self.__server_info['rosbridge']['websocket']
        ws_url = '{}?token={}'.format(ws_url, storage_token) if storage_token else ws_url
        # NOTE: roslibpy is buggy when creating more than one client, ie. calling
        #  roslibpy.Ros, a second time in the same virtual coach session (ie. from the same process)
        #  Therefore we are running the client in a separate process and channeling the incoming
        #  msgs to subscribed callbacks in this process through a multiprocessing.Pipe
        try:
            self.__ros_client = RosBridgeHandlerProcess()
            self.__ros_client.initialize(ws_url)

            self.__ros_client.subscribe_topic(self.__config['ros']['status'], 'std_msgs/String',
                                              self.__on_status)

            self.__ros_client.subscribe_topic(self.__config['ros']['error'],
                                              'cle_ros_msgs/CLEError', self.__on_error)
        # pylint: disable=broad-except
        except Exception:
            self.__logger.info('Connection with rosbridge server could not be established. '
                               'Some functionalities will be disabled')

        # success, simulation is launched
        self.__logger.info('Ready.')
        return True

    def start(self):
        """
        Attempt to start the simulation by transitioning to the "started" state.
        """
        self.__set_state('started')

    def pause(self):
        """
        Attempt to pause the simulation by transitioning to the "paused" state.
        """
        self.__set_state('paused')

    def stop(self):
        """
        Attempt to stop the simulation by transitioning to the "stopped" state.
        """
        self.__set_state('stopped')

    def register_status_callback(self, callback):
        """
        Register a status message callback to be called whenever a simulation status message
        is received. This functionality is only available on installations with native ROS
        support.

        :param callback: The callback function to be invoked.
        """

        # ensure the simulation is started and valid
        if not self.__server or not self.__sim_url:
            raise Exception(
                "Simulation has not been created, cannot set state!")

        # make sure the callback is not registered already, warn the user if it is
        if callback in self.__status_callbacks:
            self.__logger.warning(
                'Attempting to register duplicate status callback, ignoring.')
            return

        # register the callback
        self.__status_callbacks.append(callback)
        self.__logger.info('Status callback registered.')

    def __set_state(self, state):
        """
        Internal helper to attempt to transition the simulation to the given state. We cannot
        guarantee current state at this point because we do not subscribe to simulation state
        and the user may be able to change things in the graphical frontend.

        :param state: The target state to transition to, see the simulation lifecycle in
                      ExDBackend for valid states.
        """

        assert isinstance(state, string_types)

        # ensure the simulation is started and valid
        if not self.__server or not self.__sim_url:
            raise Exception(
                "Simulation has not been created, cannot set state!")

        # attempt to transition the state
        self.__logger.info('Attempting to transition to state: %s', state)
        url = '%s/%s' % (self.__sim_url,
                         self.__config['simulation-services']['state'])
        status_code, _ = self.__http_client.put(url, body={'state': state})

        # check the return code, this will return OK if the REST call succeeds
        if status_code != http.client.OK:
            raise Exception(
                "Unable to set simulation state, HTTP status %s" % status_code)
        self.__logger.info('Simulation state: %s', state)

    def __on_error(self, msg):
        """
        Function to log ROS CLE error messages.
        :param msg A CLEError message
        """
        error_msg = "There was a %(type)s error resulting from the %(source)s." \
                    " The full error is below:\n %(msg)s" % {'type': msg['errorType'],
                                                             'source': msg['sourceType'],
                                                             'msg': msg['message']}
        self.__logger.error(error_msg)

    def __on_status(self, msg):
        """
        Internal function to receive ROS status messages for this simulation. Loading or shutdown
        messages will be logged. Simulation status messages will be forwarded to any registered
        callbacks.

        :param msg: A ROS String message representation of a JSON status message for the frontend.
        """

        # status messages are JSON strings sent to the frontend, decode to a Python dict
        status = json.loads(msg['data'])

        if 'action' in status:
            return

        # a loading or shutdown message from the simulation, log it to console, but don't propagate
        if 'progress' in status:

            # ignore duplicate done messages that are used to clear progress bars on the frontend
            if 'subtask' not in status['progress']:
                return

            if status['progress']['subtask'] == self.__previous_subtask:
                return

            self.__previous_subtask = status['progress']['subtask']
            self.__logger.info('[%s] %s', status['progress']
                               ['task'], status['progress']['subtask'])

        # an actual simulation status / info message, check if we have stopped and forward it along
        else:

            # forward the message along to any callbacks that have been registered
            for callback in self.__status_callbacks:
                callback(status)

            # if the simulation has stopped clear all callbacks and close rosbridge connection,
            # this simulation instance should not be reused
            if status['state'] in ['stopped', 'halted']:
                self.__status_callbacks[:] = []
                if self.__ros_client:
                    self.__ros_client.close()
                self.__logger.info('Simulation has been stopped.')

    def get_state(self):
        """
        Returns the current simulation state.
        """
        if not self.__server or not self.__sim_url:
            raise Exception(
                "Simulation has not been created, cannot get simulation state!")

        url = '%s/%s' % (self.__sim_url,
                         self.__config['simulation-services']['state'])
        status_code, content = self.__http_client.get(url)

        if status_code != http.client.OK:
            raise Exception("Unable to get current simulation state, HTTP status %s"
                            % status_code)

        return str(json.loads(content)['state'])

    def __get_simulation_scripts(self, script_type):
        """
        Internal helper to retrieve all simulation scripts (transfer-functions, state-machines and
        brain) defined in a simulation.

        :param script_type: The script type to be retrieved. Either transfer-functions,
                            state-machines or the brain
        """
        assert isinstance(script_type, string_types)

        if not self.__server or not self.__sim_url:
            raise Exception(
                "Simulation has not been created, cannot get %s!" % script_type)

        if script_type not in self.__config['simulation-scripts']:
            raise ValueError("Script type %s not defined. Possible values are: %s"
                             % (script_type, ", ".join(self.__config['simulation-scripts'])))

        self.__logger.info("Attempting to retrieve %s", script_type)

        url = '%s/%s' % (self.__sim_url,
                         self.__config['simulation-scripts'][script_type])

        status_code, content = self.__http_client.get(url)

        if status_code != http.client.OK:
            raise Exception("Unable to get simulation %s, HTTP status %s"
                            % (script_type, status_code))
        return json.loads(content)

    def __get_script(self, script_name, script_type):
        """
        Internal helper to generalize the GET call for all script types.

        :param script_name: The name of the script to be retrieved
        :param script_type: The type of the script to be retrieved (transfer-function, brain,
                            state-machine)
        """
        assert isinstance(script_name, string_types)
        script_type_print_format = ' '.join(script_type.split('-')).title()

        self.__logger.info('Attempting to retrieve %s: %s', script_type_print_format,
                           script_name)

        if not self.__server or not self.__sim_url:
            raise Exception("Simulation has not been created, cannot get %s!"
                            % script_type_print_format)

        defined_scripts = self.__get_simulation_scripts(script_type)['data']
        if script_name not in defined_scripts:
            raise ValueError('%s: "%s" does not exist. Please check the %ss ids: \n%s'
                             % (script_type_print_format, script_name, script_type_print_format,
                                str('\n').join(list(defined_scripts.keys()))))

        return defined_scripts[script_name]

    def __set_script(self, script_type, script, script_name='', new=False):
        """
        Attempt to add a new or edit an existing simulation script. If a script is being set while
        the simulation is started, then the simulation will be temporarily paused and restarted
        again after setting the new script. If a script is being set while the simulation is paused,
        then no state transition will occur and the new script will be directly set. This ensures
        that after setting a new script, the simulation will be in the same state as before.

        :param script_type: A string containing the type of script to be set.
        :param script_name: A string containing the name of the script that is going to be modified.
        :param script: A string containing the code of the new script.
        :param new: A flag indicating whether the script is being newly added or modified.
        """
        assert isinstance(script_name, string_types)
        assert isinstance(script, string_types)

        script_type_display = ' '.join(script_type.split('-')).title()

        if not self.__server or not self.__sim_url:
            raise Exception(
                "Simulation has not been created, cannot set %s!" % script_type_display)

        defined_scripts = self.__get_simulation_scripts(script_type)['data']

        self.__logger.info('Attempting to set %s %s', script_type_display, script_name)
        url = '%s/%s/%s' % (self.__sim_url, self.__config['simulation-scripts'][script_type],
                            script_name)
        started = False

        # check for current simulation state and pause simulation if it's running
        if self.get_state() == 'started':
            started = True
            self.pause()

        try:

            if new:
                if script_type == 'transfer-function':
                    url = '%s/%s' % (self.__sim_url,
                                     self.__config['simulation-scripts'][script_type])
                    status_code, _ = self.__http_client.post(url, body=script)
                else:
                    url = '%s/%s/%s' % (self.__sim_url,
                                        self.__config['simulation-scripts'][script_type],
                                        script_name)
                    status_code, _ = self.__http_client.put(url, body=script)

            # keep reference to the old script body in case of syntax errors
            else:
                script_original = defined_scripts[script_name]
                url = '%s/%s/%s' % (self.__sim_url,
                                    self.__config['simulation-scripts'][script_type], script_name)
                status_code, _ = self.__http_client.put(url, body=script)
            if status_code != http.client.OK:
                raise Exception("Unable to set %s, HTTP status %s"
                                % (script_type_display, status_code))
            self.__logger.info("%s '%s' successfully updated", script_type_display, script_name)
        except HTTPError as err:
            self.__logger.info(err)
            if not new:
                self.__logger.info(
                    'Attempting to restore the old %s.', script_type_display)
                status_code, _ = self.__http_client.put(
                    url, body=script_original)
                if status_code != http.client.OK:
                    raise Exception("Unable to restore %s, HTTP status %s"
                                    % (script_type_display, status_code))

            raise Exception("Error detected. The Simulation is now paused.")

        # resume simulation if it was initially running
        if started:
            self.start()

    def __delete_script(self, script_type, script_name):
        """
        Deletes a simulation script (Transfer Function or State Machine).

        :param script_type: A string containing the type of the script to be deleted.
        :param script_name: A string containing the name of the script to be deleted.
        """
        assert isinstance(script_name, string_types)

        script_type_display = ' '.join(script_type.split('-')).title()

        if not self.__server or not self.__sim_url:
            raise Exception(
                "Simulation has not been created, cannot set %s!" % script_type_display)

        script_list = self.__get_simulation_scripts(script_type)['data']

        if script_name not in script_list:
            raise ValueError('%s: "%s" does not exist. Please check the %s ids: \n%s'
                             % (script_type_display, script_name, script_type_display,
                                str('\n'.join(script_list))))

        self.__logger.info('Attempting to delete %s %s', script_type_display, script_name)
        url = '%s/%s/%s' % (self.__sim_url, self.__config['simulation-scripts'][script_type],
                            script_name)
        status_code = self.__http_client.delete(url, body=script_name)

        if status_code != http.client.OK:
            raise Exception("Unable to delete %s, HTTP status %s"
                            % (script_type_display, status_code))
        self.__logger.info("%s '%s' successfully deleted", script_type_display, script_name)

    def print_transfer_functions(self):
        """
        Prints a list of the transfer-function names defined in the experiment.
        """
        printStr = '\n'.join(list(self.__get_simulation_scripts(
            'transfer-function')['data'].keys()))

        print(printStr)

    def print_state_machines(self):
        """
        Prints a list of the state-machine names defined in the experiment.
        """
        printStr = "\n".join(list(self.__get_simulation_scripts(
            'state-machine')['data'].keys()))

        print(printStr)

    def get_transfer_function(self, transfer_function_name):
        """
        Gets the transfer function body for a given transfer function name.

        :param transfer_function_name: A string containing the name of the transfer function.
        """
        return self.__get_script(transfer_function_name, 'transfer-function')

    def edit_transfer_function(self, transfer_function_name, transfer_function):
        """
        Modify an existing Transfer Function by updating the script.

        :param transfer_function_name: A string containing the name of the transfer function to be
                                      edited.
        :param transfer_function: A string containing the new transfer function code.
        """
        self.__set_script('transfer-function', transfer_function,
                          script_name=transfer_function_name)

    def add_transfer_function(self, transfer_function):
        """
        Adds a new transfer function to the simulation.

        :param transfer_function: A string containing the new transfer function code.
        """
        self.__set_script('transfer-function', transfer_function, new=True)

    def delete_transfer_function(self, transfer_function_name):
        """
        Deletes a transfer function.

        :param transfer_function_name: A string containing the name of the transfer function to be
                                       deleted.
        """
        self.__delete_script('transfer-function', transfer_function_name)

    def __save_experiment_data(self, experiment_data_type, experiment_data,
                               method='put', backend=False):
        """
        Saves data related to the experiment.
        Url format: in the format http://proxy_url/proxy/{exp-id}/brain
        or if backend has been set to true
          http://sim_url/{exp-id}/sdf-world
        :param experiment_data_type: the type of experiment data to save (i.e. 'transfer-function',
                                     'state-machine', 'brain' or 'sdf-world')
        :param experiment_data: the experiment data to be saved
        :param method: the http request to be executed. Default is: PUT
        :param backend: whether this is a backend call or not
        """
        if backend:
            url = '%s/%s' % (self.__sim_url,
                             self.__config['simulation-scripts'][experiment_data_type])
        else:
            url = '%s/%s/%s' % (self.__config['proxy-services']['save-data'],
                                self.__experiment_id,
                                self.__config['proxy-save'][experiment_data_type])
        try:
            method_fun = getattr(self.__http_client, method)
            status_code, _ = method_fun(url, body=experiment_data)

            if status_code != http.client.OK:
                raise Exception('Error status code %s' % status_code)
            self.__logger.info("Saved %s.", experiment_data_type)
        except Exception as err:
            self.__logger.info(err)
            raise Exception("Failed to save %s." % experiment_data_type)

    def save_transfer_functions(self):
        """
        Saves the current transfer functions to the storage
        """
        transfer_functions = list(self.__get_simulation_scripts(
            'transfer-function')['data'].keys())
        transfer_functions_list = []
        for tf in transfer_functions:
            transfer_functions_list.append(self.get_transfer_function(str(tf)))

        self.__save_experiment_data('transfer-function',
                                    {'experiment': self.__experiment_id,
                                     'transferFunctions': transfer_functions_list})

    def save_state_machines(self):
        """
        Saves the current state machines to the storage
        """
        state_machines_dict = {}
        for sm in list(self.__get_simulation_scripts('state-machine')['data'].keys()):
            state_machines_dict[sm] = self.get_state_machine(str(sm))

        self.__save_experiment_data('state-machine', {'experiment': self.__experiment_id,
                                                      'stateMachines': state_machines_dict})

    def save_brain(self):
        """
        Saves the current brain script and populations to the storage
        """
        pynn_script = self.get_brain()
        populations = self.get_populations()

        # Remove the regex entry from the populations dictionary if it is available. The regex
        # entry is provided by the frontend to check for duplicate population names and should be
        # refactored.
        if 'regex' in list(populations.values())[0]:
            for pop in populations:
                del populations[pop]['regex']

        self.save_transfer_functions()
        self.__save_experiment_data('brain', {'brain': pynn_script,
                                              'populations': populations})

    def save_world(self):
        """
        Saves the current sdf world to the storage
        """
        return self.__save_experiment_data('sdf-world', {}, method='post', backend=True)

    def get_state_machine(self, state_machine_name):
        """
        Gets the State Machine body for a given state machine name.

        :param state_machine_name: A string containing the name of the state machine.
        """
        return self.__get_script(state_machine_name, 'state-machine')

    def edit_state_machine(self, state_machine_name, state_machine):
        """
        Modify an existing State Machine by updating the script.

        :param state_machine_name: A string containing the name of the state machine to be edited.
        :param state_machine: A string containing the new state machine code.
        """
        self.__set_script('state-machine', state_machine,
                          script_name=state_machine_name)

    def add_state_machine(self, state_machine_name, state_machine):
        """
        Adds a new State Machine to the simulation.

        :param state_machine_name: A string containing the name of the state machine to be added.
        :param state_machine: A string containing the new state machine code.
        """
        self.__set_script('state-machine', state_machine,
                          script_name=state_machine_name, new=True)

    def delete_state_machine(self, state_machine_name):
        """
        Deletes a state machine.

        :param state_machine_name: A string containing the name of the state machine to be deleted.
        """
        self.__delete_script('state-machine', state_machine_name)

    def __set_populations(self, neural_population, change_population):
        """
        Internal helper method to help set either the brain script or the neural populations.

        :param neural_population: A dictionary containing neuron indices and is indexed by
                                  population names. Neuron indices could be defined by individual
                                  integers, lists of integers or python slices.
                                  Python slices are defined by a dictionary containing the 'from',
                                  'to' and 'step' values.
        :param change_population: A flag to select an action on population name change. Currently,
                                  possible values are: 0 ask user for permission to replace;
                                  1 (permission granted) replace old name with a new one;
                                  2 proceed with no replace action.
        """
        assert isinstance(neural_population, dict)
        assert isinstance(change_population, int)

        if not self.__server or not self.__sim_url:
            raise Exception(
                "Simulation has not been created, cannot set populations!")

        self.__logger.info('Attempting to set Populations')

        # keep reference to the old script body in case of syntax errors
        old_populations = self.get_populations()

        # Get old brain parameters to reuse them
        old_data_type = self.__get_simulation_scripts('brain')['data_type']
        old_brain_type = self.__get_simulation_scripts('brain')['brain_type']
        body = {'brain_type': old_brain_type, 'brain_populations': neural_population,
                'data_type': old_data_type, 'change_population': change_population}

        url = '%s/%s' % (self.__sim_url,
                         self.__config['simulation-scripts']['populations'])
        started = False

        # check for current simulation state and pause simulation if it's running
        if self.get_state() == 'started':
            started = True
            self.pause()
        try:
            status_code, _ = self.__http_client.put(url, body=body)
            if status_code != http.client.OK:
                raise Exception(
                    "Unable to set Populations, HTTP status %s" % status_code)
            self.__logger.info("Populations successfully updated.")
        except HTTPError as err:
            self.__logger.info(err)
            self.__logger.info('Attempting to restore the old Populations.')
            body['brain_populations'] = old_populations
            body['data_type'] = old_data_type
            body['brain_type'] = old_brain_type

            status_code, _ = self.__http_client.put(url, body=body)
            if status_code != http.client.OK:
                raise Exception(
                    "Unable to restore Brain, HTTP status %s" % status_code)

            raise Exception("Error detected. The Simulation is now paused and the old script is "
                            "restored.")
        # resume simulation if it was initially running
        if started:
            self.start()

    def __set_brain(self, brain_script, neural_population):
        """
        Internal helper method to help set either the brain script or the neural populations.

        :param brain_script: A string containing a python script that defines a pyNN neural network.
        :param neural_population: A dictionary containing neuron indices and is indexed by
                                   population names. Neuron indices could be defined by individual
                                   integers, lists of integers or python slices.
        """

        assert isinstance(brain_script, (string_types, string_types))
        assert isinstance(neural_population, dict)

        if not self.__server or not self.__sim_url:
            raise Exception(
                "Simulation has not been created, cannot set Brain!")

        self.__logger.info('Attempting to set Brain')

        # keep reference to the old script body in case of syntax errors
        old_brain = self.get_brain()

        # Get old brain parameters to reuse them
        old_data_type = self.__get_simulation_scripts('brain')['data_type']
        old_brain_type = self.__get_simulation_scripts('brain')['brain_type']
        old_populations = self.get_populations()
        # change_population is set to 2, which means proceed with no replace_population action
        body = {'data': brain_script, 'data_type': old_data_type,
                'brain_type': old_brain_type, 'brain_populations': neural_population}

        url = '%s/%s' % (self.__sim_url,
                         self.__config['simulation-scripts']['brain'])
        started = False

        if self.get_state() == 'started':
            started = True
            self.pause()
        # check for current simulation state and pause simulation if it's running
        try:
            status_code, _ = self.__http_client.put(url, body=body)
            if status_code != http.client.OK:
                raise Exception(
                    "Unable to set Brain, HTTP status %s" % status_code)
            self.__logger.info("Brain successfully updated.")
        except HTTPError as err:
            self.__logger.info(err)
            self.__logger.info('Attempting to restore the old Brain.')
            body['data'] = old_brain
            body['populations'] = old_populations
            status_code, _ = self.__http_client.put(url, body=body)
            if status_code != http.client.OK:
                raise Exception(
                    "Unable to restore Brain, HTTP status %s" % status_code)

            raise Exception("Error detected. The Simulation is now paused and the old script is "
                            "restored.")

        # resume simulation if it was initially running
        if started:
            self.start()

    def get_brain(self):
        """
        Gets the brain script.
        """
        return self.__get_simulation_scripts('brain')['data']

    def edit_brain(self, brain_script):
        """
        Edits the brain script defined in the simulation and keeps the defined populations. Calling
        this method will not change brain populations.

        :param brain_script: A string containing the new pyNN script.
        """
        self.__set_brain(brain_script, self.get_populations())

    def get_populations(self):
        """
        Gets the Neuron populations defined within the brain as a dictionary indexed by population
        names.
        """
        return self.__get_simulation_scripts('brain')['brain_populations']

    def edit_populations(self, populations):
        """
        Modifies the neuron populations and replaces old population names with new ones in the
        transfer functions automatically.

        :param populations: A dictionary containing neuron indices and is indexed by population
                            names. Neuron indices could be defined by individual integers, lists of
                            integers or python slices. Python slices are defined by a dictionary
                            containing the 'from', 'to' and 'step' values.
        """
        assert isinstance(populations, dict)
        self.__set_populations(populations, False)

    def reset(self, reset_type):
        """
        Resets the simulation according to the type the user wants. Successful reset will pause the
        simulation.

        :param reset_type: The reset type the user wants to be performed. Possible values are full,
                           robot_pose and world. The possible reset types are stored in the
                           config file.
        """

        assert isinstance(reset_type, (string_types, string_types))

        # NRRPLT-7855
        if reset_type in ['full', 'world']:
            raise ValueError('Reset %s temporarily disabled due to known Gazebo issue' % reset_type)

        if reset_type not in self.__config['reset-services']:
            raise ValueError('Undefined reset type. Possible values are: %s'
                             % ", ".join(list(self.__config['reset-services'].keys())))

        # pausing simulation before attempting to reset
        self.pause()

        self.__logger.info("Attempting to reset %s", reset_type)
        url = '%s/%s/%s' % (self.__sim_url, self.__experiment_id,
                            self.__config['simulation-services']['reset'])
        body = {'resetType': self.__config['reset-services'][reset_type]}
        status_code, _ = self.__http_client.put(url, body=body)

        # check the return code, this will return OK if the REST call succeeds
        if status_code != http.client.OK:
            self.start()
            raise Exception(
                "Unable to reset simulation, HTTP status %s" % status_code)
        self.__logger.info('Reset completed. The simulation has been paused and will not be started'
                           ' automatically.')

    def get_csv_last_run_file(self, file_name):
        """
        Retrieves a csv file content for the last simulation run.

        :param file_name: The name of csv file for which to retrieve the content.
        """
        return self.__vc.get_csv_last_run_file(self.__experiment_id, file_name)

    def __send_recorder_cmd(self, cmd):
        """
        Internal helper to attempt to send a command to the recorder

        :param cmd: A recorder command supported by ExDBackend.

        """

        assert isinstance(cmd, string_types)

        # ensure the simulation is started and valid
        if not self.__server or not self.__sim_url:
            raise Exception(
                "Simulation has not been created, cannot receive recorder command!")

        # attempt to send a command to the recorder
        self.__logger.info('Attempting to send a comment to the recorder: %s', cmd)
        url = '%s/%s/%s' % (self.__sim_url,
                            self.__config['simulation-services']['recorder'],
                            cmd)

        status_code, result = self.__http_client.post(url, body=cmd)

        # check the return code, this will return OK if the REST call succeeds
        if status_code != http.client.OK:
            raise Exception(
                "Unable to send command to recorder, HTTP status %s" % status_code)

        return result

    def start_recording(self):
        """
        Start recording.
        """
        self.__send_recorder_cmd('start')
        self.__logger.info('Start recording')

    def stop_recording(self, save, description=None):
        """
        Stop recording and save the file if save is True. An optional description can be passed.

        :param save: True if the recording needs to be saves.
        :param description: If provided a description of recording to be saved.

        """
        self.__send_recorder_cmd('stop')

        if save is True:
            result = self.__send_recorder_cmd('save')
            if description is not None:
                json_result = json.loads(result)
                filename = json_result['filename']
                filename = os.path.splitext(filename)[0]
                filename = filename + '.txt'
                self.__vc.set_experiment_file(self.__experiment_id,
                                              os.path.join('recordings',
                                                           filename),
                                              description)

        self.__send_recorder_cmd('reset')

    def pause_recording(self):
        """
        Pause recording.
        """
        self.__send_recorder_cmd('stop')

    def unpause_recording(self):
        """
        Un-pause recording.
        """
        self.__send_recorder_cmd('start')
