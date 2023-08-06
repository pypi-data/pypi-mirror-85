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
Virtual Coach main entry point for interacting with the experiment list and launching simulations.
"""

# pylint: disable=W0622

from __future__ import print_function

from builtins import str
from builtins import object

import json
import logging
import getpass
import http.client
import os
import zipfile
import tempfile

import requests
from urllib import parse as urlparse

from copy import copy

from datetime import datetime, timedelta
from collections import defaultdict
from dateutil import parser, tz

from texttable import Texttable
from six import string_types
from future import standard_library

from pynrp.config import Config
from pynrp.simulation import Simulation
from pynrp.requests_client import RequestsClient

standard_library.install_aliases()

logger_format = '%(levelname)s: [%(asctime)s - %(name)s] %(message)s'
logging.basicConfig(format=logger_format, level=logging.INFO)
logger = logging.getLogger('VirtualCoach')


class VirtualCoach(object):
    """
    Provides the user with methods for interacting with the experiment list, providing
    functionality similar to the graphical frontend experiment list webpage. Allows the user to
    view available experiments, query currently running experiments, launch a simulation, and more.
    """

    def __init__(self, environment='http://localhost:9000', oidc_username=None, oidc_password=None,
                 oidc_token=None, storage_username=None, storage_password=None):
        """
        Instantiates the Virtual Coach by loading the configuration file and logging into OIDC for
        the given user. This will only fail if the config file is invalid or if the user
        credentials are incorrect. The user will be prompted to provide a password if they have not
        logged in recently.

        :param environment: (optional) A string containing the http address of the server running
                            the NRP. The default value is localhost:9000
        :param oidc_username: (optional) A string representing the OIDC username for the current
                              user, required if the provided environment requires OIDC
                              authentication and no token is provided.
        :param oidc_password: (optional) A string representing the OIDC Server password. If
                                 not supplied, the user will be prompted to enter a password.
        :param oidc_token: (optional) A string representing the OIDC token for the current
                              user, required if the selected environment requires OIDC
                              and the username is not provided.
        :param storage_username: (optional) A string representing the Storage Server username. It is
                                 required if the user wants to have access to the storage server to
                                 clone experiments and launch cloned experiments.
        :param storage_password: (optional) A string representing the Storage Server password. If
                                 not supplied, the user will be prompted to enter a password.
        """
        assert isinstance(environment, (string_types, type(None)))
        assert isinstance(oidc_username, (string_types, type(None)))
        assert isinstance(oidc_token, (string_types, type(None)))
        assert isinstance(storage_username, (string_types, type(None)))

        # parse and load the config file before any OIDC actions
        self.__config = Config(environment)
        self.__oidc_username = oidc_username
        self.__storage_username = storage_username

        # authorize client into oidc or storage server
        token = ''
        if oidc_username or oidc_token:
            if oidc_username:
                logger.info('Logging into OIDC as: %s', oidc_username)
                if not oidc_password:
                    oidc_password = getpass.getpass(prompt='input your OIDC password: ')
                token = self.__get_oidc_token(oidc_username, oidc_password)
            else:
                if self.__oidc_token_is_valid(token):
                    logger.info('Using provided token for OIDC server authorization')
                    token = oidc_token
                else:
                    raise Exception('Provided OIDC token is invalid, VirtualCoach cannot be '
                                    'instantiated.')
        elif storage_username:
            logger.warning('No OIDC username supplied, simulation services will fail if OIDC is '
                           'enabled in this environment (%s).', environment)
            logger.info('Logging into the Storage Server as: %s', storage_username)
            if not storage_password:
                storage_password = getpass.getpass()
            token = self.__get_storage_token(storage_username, storage_password)
        else:
            raise Exception('Virtual Coach instantiated without storage server credentials or oidc'
                            'credentials. You have to provide either one with the keywords '
                            '"storage_username" or "oidc_username" to have access to Experiment '
                            'files.')

        self.__storage_token = token
        self.__http_headers = {'Content-Type': 'application/json',
                               'Authorization': 'Bearer %s' % token}
        self.__http_client = RequestsClient(self.__http_headers)

        # if the config is valid and the login doesn't fail, we're ready
        logger.info('Ready.')

    def __oidc_token_is_valid(self, token):
        '''
        check if a given oidc token is valid

        :param token: token to validate as a string
        '''

        response = requests.post('https://services.humanbrainproject.eu/oidc/tokeninfo',
                                 data=urlparse.urlencode({'access_token': token}),
                                 headers={'Content-Type': 'application/x-www-form-urlencoded'})

        if response.status_code != 200:
            raise Exception('OIDC token validation failed, Status Code: %d'
                            % response.status_code)

        d = json.loads(response.content)
        if 'valid' in d and not d['valid']:
            logger.info('OIDC token not valid')
            return False
        elif 'expires_in' in d and int(d['expires_in']) < 1:
            logger.info('OIDC token expired')
            return False

        logger.info('OIDC token valid')
        return True

    def __get_oidc_token(self, user_name, password):
        """
        Attempts to acquire a oidc server token based on the provided credentials

        :param user_name:  string representing the oidc Server username
        :param password:  string representing the oidc Server password
        """

        # hbp oidc request
        client_id = 'kamaji-python-client'
        oauth_url = 'https://services.humanbrainproject.eu/oidc/'

        # construct request
        query = {
            'response_type': 'token',
            'client_id': client_id,
            'redirect_uri': oauth_url + 'resources/oauth_code.html',
            'prompt': 'consent',
        }

        parts = list(urlparse.urlparse(oauth_url + 'authorize'))
        query.update(dict(urlparse.parse_qsl(parts[4])))  # 4 is the index of the query part
        parts[4] = urlparse.urlencode(query)
        authorize_url = urlparse.urlunparse(parts)

        # request token
        import mechanize
        br = mechanize.Browser()
        br.set_handle_robots(False)
        for _ in range(3):
            br.open(authorize_url)
            br.select_form(name='j_spring_security_check')

            # fill form
            # pylint: disable=unsupported-assignment-operation
            br['j_username'] = user_name
            br['j_password'] = password

            res = br.submit()

            if 'error=' not in res.geturl():
                break
        else:
            raise Exception('OIDC authorization failed. Probably you used wrong credentials.')

        # the user is forwarded to the approve page if not approved yet
        if 'access_token' not in urlparse.urlparse(res.geturl()).fragment.lower():
            br.select_form(name='confirmationForm')
            res = br.submit()

        url_with_fragment = res.geturl()

        # parse and return token
        o = urlparse.urlparse(url_with_fragment)
        frag = urlparse.parse_qs(o.fragment)
        return frag['access_token'][0]

    def __get_storage_token(self, user_name, password):
        """
        Attempts to acquire a storage server token based on the provided credentials

        :param user_name:  string representing the Storage Server username
        :param password:  string representing the Storage Server password
        """
        assert isinstance(user_name, string_types)
        assert isinstance(password, string_types)

        try:
            resp = requests.post(self.__config['proxy-services']['storage-authentication'],
                                 json={'user': user_name, 'password': password})
        # pylint: disable=broad-except
        except Exception as e:
            raise Exception('Storage Server authentication failed, with exception: {}'.format(e))

        if resp.status_code != 200:
            raise Exception('Storage Server authentication failed, Status Code: %d'
                            % resp.status_code)

        token = resp.content.decode("utf-8") if isinstance(resp.content, bytes) else resp.content

        return token

    def launch_experiment(self, experiment_id, server=None, reservation=None, cloned=True, brain_processes=1,
                          profiler='disabled'):
        """
        Attempts to launch a simulation with the given parameters. If no server is explicitly given
        then all available backend servers will be tried. Only cloned experiments to the Storage
        Server can be launched.

        :param experiment_id: The short name of the experiment configuration to launch
                              (e.g. ExDTemplateHusky).
        :param server: (optional) The full name of the server backend to launch on, if none is
                       provided, then all backend servers will be checked.
        :param reservation: (optional) A cluster reservation string if the user has reserved
                            specific resources, otherwise use any available resources.
        :param cloned: (optional) True or False depending on if the launched
                       is a cloned experiment or not.
        :param brain_processes: (optional) Number of mpi processes in the brain simulation.
        :param profiler: (optional) profiler option. Possible values are: disabled, cle_step and cprofile.
        """
        assert isinstance(experiment_id, string_types)
        assert isinstance(server, (string_types, type(None)))
        assert isinstance(reservation, (string_types, type(None)))

        # retrieve the list of cloned experiments to verify that the given id is valid for the
        # backend
        logger.info('Preparing to launch %s.', experiment_id)
        exp_list = self.__get_experiment_list(cloned)
        if experiment_id not in exp_list:
            raise ValueError('Experiment ID: "%s" is invalid, you can only launch experiments '
                             'located in your storage space. You can check your experiments with '
                             'print_cloned_experiments(). Currently you have the following '
                             'experiments available: %s' % (experiment_id, exp_list))

        # get the experiment configuration details and available servers that can be used
        available_servers = self.__get_available_server_list()
        servers = [available_server['id'] for available_server in available_servers]
        if cloned:
            experiment_conf = ""
        else:
            experiment = exp_list[experiment_id]
            experiment_conf = experiment['configuration']['experimentConfiguration']

        # if the user provided a specific server, ensure it is available before trying to launch
        if server is not None:
            logger.info('Checking server availability for: %s', server)
            if server not in servers:
                raise ValueError('Server: %s is invalid or unavailable, try again later.' % server)
            servers = [server]

        # if there are no available servers, abort
        if not servers:
            raise ValueError('No available servers for %s, try again later.' % experiment_id)

        # attempt to launch the simulation on all server targets, on success return an interface
        # to the simulation
        sim = Simulation(self.__http_client, self.__config, self)
        for server_i in servers:
            try:
                if sim.launch(experiment_id, str(experiment_conf), str(server_i),
                              reservation, cloned, self.__storage_token, brain_processes, profiler):
                    return sim

            # pylint: disable=broad-except
            except Exception as e:
                logger.exception(e)
                logger.info(e)

        # simulation launch unsuccessful, abort
        raise Exception('Simulation launch failed, consult the logs or try again later.')

    def print_templates(self, dev=False):
        """
        Prints a table of the list of experiments available on the backend environment. The printed
        list is sorted by the experiment title in the same way as the frontend webpage.

        :param dev: (optional) A boolean flag if all development maturity experiments should be
                    printed in addition to the production experiments.
        """
        assert isinstance(dev, bool)

        # retrieve and parse the current experiment list
        exp_list = self.__get_experiment_list()

        # construct the table of experiments with only minimal useful information
        table = Texttable()
        table.header(['Configuration', 'Name', 'Configuration Path', 'Description'])
        for name, v in sorted(iter(exp_list.items()), key=lambda x: x[1]['configuration']['name']):
            if v['configuration']['maturity'] != 'production' and not dev:
                continue
            if dev:
                name = '%s (%s)' % (name, v['configuration']['maturity'])
            desc = ' '.join(v['configuration']['description'].strip().split())
            table.add_row([name, v['configuration']['name'],
                           v['configuration']['experimentConfiguration'], desc])

        # display the table
        logger.info('List of production%s experiments:', '' if not dev else ' and development')
        print(table.draw())

    def print_running_experiments(self, cloned=False):
        """
        Prints a table of currently running experiments and relevant details (if any).
        """

        # retrieve and parse the current experiment list
        exp_list = self.__get_experiment_list(cloned)

        # construct a table with minimal useful information
        table = Texttable()
        table.header(['Configuration', 'Owner', 'Time', 'Timeout', 'State', 'Server'])
        for name, v in sorted(iter(exp_list.items()), key=lambda x: x[1]['configuration']['name']):

            # for any running experiments of this type
            for server in v['joinableServers']:

                # get the simulation details
                r = server['runningSimulation']

                # retrieve the user display name for the given user id, this provides a human
                # readable owner name instead of just their system id
                # use a default user name if an oidc_username hasn't been provided
                if self.__oidc_username is not None:
                    url = '%s/%s' % (self.__config['oidc']['user'], r['owner'])
                    _, content = self.__http_client.get(url)
                    owner = json.loads(content)['displayName']
                else:
                    owner = "local_user"

                # compute the approximate elapsed time of the simulation based on creation
                elapsed = str(datetime.now(tz.tzlocal()) - parser.parse(r['creationDate']))
                elapsed = elapsed[0:elapsed.rfind('.')]

                # parse the experiment timeout to display along with elapsed time
                timeout = str(timedelta(seconds=v['configuration']['timeout']))

                # add the running experiment info
                table.add_row([name, owner, elapsed, timeout, r['state'], server['server']])

        # display the table
        logger.info('All running experiments:')
        print(table.draw())

    def print_cloned_experiments(self):
        """
        Prints the list of the cloned experiments' names. Only works if the Virtual Coach was
        instantiated with Storage Server support, i.e. with Storage Server credentials
        """
        exp_list = self.__get_experiment_list(cloned=True)
        table = Texttable()
        table.header(['Name'])
        for experiment in exp_list:
            table.add_row([experiment])
        print(table.draw())

    def print_available_servers(self):
        """
        Prints a list of the available backend servers that are currently not running a simulation.
        """

        # retrieve the experiment list, and take the first list of available servers, this is the
        # same across all experiment listings
        available_servers = self.__get_available_server_list()
        servers = [server['id'] for server in available_servers]

        # add a display value if there are no available servers
        if not servers:
            servers = ['No available servers.']

        # print the list of available servers
        logger.info('Available servers:')
        print('\n'.join(servers))

        return servers

    def __get_experiment_list(self, cloned=False):
        """
        Internal helper to retrieve and parse the experiment list from the backend proxy.

        :param cloned: (optional) Flag to get cloned experiments to the storage
        """
        assert isinstance(cloned, bool)

        logger.info('Retrieving list of experiments.')
        if cloned:
            url = self.__config['proxy-services']['storage-experiment-list']
            response = requests.get(url, headers=self.__http_headers)
            # return a simple list containing only experiment names since this is the only
            # information in the dictionary anyway
            return {experiment['name']: experiment for experiment in json.loads(response.content)}
        else:
            _, response = self.__http_client.get(
                self.__config['proxy-services']['experiment-list'])

            return json.loads(response)

    def __get_available_server_list(self):
        """
        Internal helper to retrieve the available server list from the backend proxy.
        """
        logger.info('Retrieving list of available servers.')
        status_code, response = self.__http_client.get(
            self.__config['proxy-services']['available-servers'])

        if status_code != http.client.OK:
            raise Exception('Error when getting server list, Status Code: %d. Error: %s'
                            % (status_code, response))
        return json.loads(response)

    def clone_experiment_to_storage(self, exp_id):
        """
        Attempts the clone an experiment to the Storage Server. Only works if the Virtual Coach was
        instantiated with Storage Server support, i.e. Storage Server credentials

        :param exp_id: The id of the experiment to be cloned
        :returns: The ID of the cloned experiment
        """
        assert isinstance(exp_id, string_types)
        exp = self.__get_experiment_list()
        if exp_id not in list(exp.keys()):
            raise ValueError('Experiment ID: "%s" is invalid, please check the list of all '
                             'experiments: \n%s' % (exp_id, '\n'.join(list(exp.keys()))))

        exp_config_path = exp[exp_id]['configuration']['experimentConfiguration']
        body = {'expPath': exp_config_path}
        status_code, content = self.__http_client.post(
            self.__config['proxy-services']['experiment-clone'], body=body)
        if status_code != 200:
            raise Exception('Cloning Experiment failed, Status Code: %s' % status_code)
        logger.info('Experiment "%s" cloned successfully', exp_id)
        return content.decode()

    def delete_cloned_experiment(self, exp_id):
        """
        Attempts to delete a cloned experiment from the storage_server

        :param exp_id: The id of the experiment to be deleted
        """
        exp_list = self.__get_experiment_list(cloned=True)
        if exp_id not in exp_list:
            raise ValueError('Experiment ID: "%s" is invalid, the experiment does not exist in your'
                             ' storage. Please check the list of all experiments: \n%s'
                             % (exp_id, exp_list))
        self.__http_client.delete(self.__config['proxy-services']['experiment-delete'] + exp_id,
                                  body={})
        logger.info('Experiment "%s" deleted successfully', exp_id)

    def clone_cloned_experiment(self, experiment_id):
        """
        Attempts to clone a cloned experiment to the Storage Server.

        :param experiment_id: The id of the cloned experiment to be cloned. E.g. benchmark_p3dx_1
        :returns: A dict containing the ID of the cloned experiment and the ID of the original
                  experiment. Dict Keys are: 'clonedExp' and 'originalExp'
        """
        assert isinstance(experiment_id, string_types)

        exp_list = self.__get_experiment_list(cloned=True)
        if experiment_id not in exp_list:
            raise ValueError('Experiment id : %s is invalid, please check the list '
                             'of all Experiments ids:\n%s' % (experiment_id, '\n'.join(exp_list)))

        # Raise Error in case no storage server token available. To get the token, the VC has to be
        # instantiated with the storage_username parameter
        if self.__storage_username is None and self.__oidc_username is None:
            raise ValueError('No Storage Server credentials found. '
                             'To be able to clone experiments, you have to instantiate the '
                             'Virtual Coach either with the storage_username parameter or '
                             'the oidc_username parameter and login successfully')

        res = requests.post('%s/%s' % (self.__config['proxy-services']['experiment-clone'],
                                       experiment_id),
                            headers=self.__http_headers)
        if res.status_code != 200:
            raise Exception('Cloning Experiment failed, Status Code: %s' % res.status_code)
        logger.info('Experiment "%s" cloned successfully', experiment_id)
        return res.content

    def print_csv_experiment_runs(self, exp_id):
        """
        Prints the list of ids of experiment runs that generated CSV files. The ids can be used
        to retrieve the CSV data

        :param exp_id: The experiment id for which to retrieve the list of CSV simulation runs
        """
        csv_files = self.__get_available_CSV_files(exp_id)

        table = Texttable()
        table.header(['Run id', 'Date', 'Bytes'])
        table.set_cols_align(['r', 'c', 'r'])

        for i, run_date in enumerate(sorted(csv_files.keys())):
            run_size = sum(file['size'] for file in list(csv_files[run_date].values()))
            table.add_row([i, run_date, run_size])

        logger.info('List of simulation runs')
        print(table.draw())

    def print_csv_experiment_run_files(self, exp_id, run_id):
        """
        Prints the list of CSV files for a given experiment run

        :param exp_id: The experiment id for which to retrieve the list of CSV files
        :param run_id: The run id for which to retrieve the list of CSV files
        """
        csv_files = self.__get_available_CSV_files(exp_id)

        table = Texttable()
        table.header(['File', 'Size'])
        table.set_cols_align(['l', 'r'])

        sorted_runs = sorted(csv_files.keys())
        if not 0 <= run_id < len(sorted_runs):
            raise Exception('Could not find run %i, %i runs were found' %
                            (run_id, len(sorted_runs)))

        for csv_file in list(csv_files[sorted_runs[run_id]].values()):
            table.add_row([csv_file['name'], csv_file['size']])

        logger.info('Run %i list of files.', run_id)
        print(table.draw())

    def print_csv_last_run_files(self, exp_id):
        """
        Prints the list of CSV files for the last run of an experiment

        :param exp_id: The experiment id for which to retrieve the list of CSV files
        """
        csv_files = self.__get_available_CSV_files(exp_id)

        table = Texttable()
        table.header(['File', 'Size'])
        table.set_cols_align(['l', 'r'])

        sorted_runs = sorted(csv_files.keys())
        if not sorted_runs:
            raise Exception('Could not find any run')

        for csv_file in list(csv_files[sorted_runs[-1]].values()):
            table.add_row([csv_file['name'], csv_file['size']])

        logger.info('Last run list of files')
        print(table.draw())

    def get_csv_experiment_run_file(self, exp_id, run_id, file_name):
        """
        Retrieves a CSV file content

        :param exp_id: The experiment id
        :param run_id: The run id
        :param file_uuid: The file uuid
        """
        csv_files = self.__get_available_CSV_files(exp_id)
        sorted_runs = sorted(csv_files.keys())
        if not 0 <= run_id < len(sorted_runs):
            raise Exception('Could not find run %i, %i runs were found' %
                            (run_id, len(sorted_runs)))

        if file_name not in csv_files[sorted_runs[run_id]]:
            file_names = ', '.join(f['name'] for f in list(csv_files[sorted_runs[run_id]].values()))
            raise Exception('Could not find file \'%s\' in run %i, available file names are: %s' %
                            (file_name, run_id, file_names))

        file_uuid = csv_files[sorted_runs[run_id]][file_name]['uuid']
        return self.__get_csv_file_content(exp_id, file_uuid)

    def get_csv_last_run_file(self, exp_id, file_name):
        """
        Retrieves a CSV file content for the last run

        :param exp_id: The experiment id
        :param file_name: The file name
        """

        csv_files = self.__get_available_CSV_files(exp_id)
        sorted_runs = sorted(csv_files.keys())
        if not sorted_runs:
            raise Exception('Could not find any run')

        if file_name not in csv_files[sorted_runs[-1]]:
            file_names = ', '.join(
                file['name'] for file in list(csv_files[sorted_runs[-1]].values()))
            raise Exception('Could not find file \'%s\' in last run, available file names are: %s' %
                            (file_name, file_names))

        file_uuid = csv_files[sorted_runs[-1]][file_name]['uuid']
        return self.__get_csv_file_content(exp_id, file_uuid)

    def __get_available_CSV_files(self, experiment_id):
        """
        Internal helper to retrieve the list of CSV files available for an experiment

        :param experiment_id: The experiment id for which to retrieve the list of CSV files
        """
        response = requests.get(self.__config['proxy-services']['csv-files'] % (experiment_id,),
                                headers=self.__http_headers)

        if response.status_code != http.client.OK:
            raise Exception('Error when getting CSV files Status Code: %d. Error: %s'
                            % (response.status_code, response))
        csv_files = json.loads(response.content)
        distinct_runs = defaultdict(dict)
        for csv_file in csv_files:
            distinct_runs[csv_file['folder']][csv_file['name']] = csv_file
        return distinct_runs

    def __get_csv_file_content(self, exp_id, file_uuid):
        """
        Internal helper method to retrieve a CSV file content

        :param exp_id: The experiment id for which to retrieve the CSV file content
        :param file_uuid: The file uuid for which to retrieve the content
        """
        logger.info('Retrieving CSV file.')

        response = requests.get(self.__config['proxy-services']['experiment-file'] %
                                (exp_id, file_uuid),
                                headers=self.__http_headers)

        if response.status_code != http.client.OK:
            raise Exception('Error when getting CSV file Status Code: %d. Error: %s'
                            % (response.status_code, response))

        return response.content

    def set_experiment_file(self, exp_id, file_name, file_content):
        """
        Create/Update a file with passed file content

        :param exp_id: The experiment id
        :param file_name: The file name
        :param file_content: The content of the file
        """

        url = self.__config['proxy-services']['experiment-file'] % (exp_id, file_name)
        url = '%s?byname=true' % url

        file_headers = copy(self.__http_headers)
        file_headers['Content-Type'] = 'text/plain'
        response = requests.post(url, data=file_content, headers=file_headers)

        if response.status_code != http.client.OK:
            raise Exception('Error when setting file: %d. Error: %s'
                            % (response.status_code, response))

        return response.content

    def import_experiment(self, path):
        """
        Imports an experiment folder, possibly a zipped folder, into user storage

        :param path: path to the experiment folder or to the zip file to be imported
        :type path: str
        """
        if not isinstance(path, string_types):
            raise TypeError('The provided argument is not a string.')
        if not os.path.isfile(path) and not os.path.isdir(path):
            raise ValueError('The file or folder named %(path)s does not exist.' % {'path': path})

        url = self.__config['proxy-services']['experiment-import']
        file_headers = copy(self.__http_headers)
        file_headers['Content-Type'] = 'application/octet-stream'

        if os.path.isdir(path):
            # Handles an experiment folder
            content = VirtualCoach.__get_directory_content(path)
        else:
            # Handles a zip file
            try:
                content = open(path, 'rb').read()
            except Exception as e:
                logger.error('The file %s could not be open', path)
                raise e

        response = requests.post(url, data=content, headers=file_headers)
        # pylint: disable=no-member
        if response.status_code != requests.codes.ok:
            raise Exception('Error when importing experiment: %d. Error: %s'
                            % (response.status_code, response))
        return response

    @staticmethod
    def __zip_directory(dirpath, zip_filehandle):
        """
        Internal helper function
        It zips the target directory

        :param dirpath: Path to the experiment folder to be zipped
        :param zip_filehandle: Handle of the zip file to be populated
        """
        dirpath = os.path.abspath(dirpath)
        dirname = os.path.dirname(dirpath)
        basename = os.path.basename(dirpath)
        os.chdir(dirname)
        for root, _, files in os.walk(basename):
            for f in files:
                zip_filehandle.write(os.path.join(root, f))

    @staticmethod
    def __get_directory_content(dirpath):
        """
        Internal helper function
        It zips the target folder and returns its content

        :param dirpath: path to the experiment folder to be zipped
        """
        temp = tempfile.mktemp()
        zip_file = zipfile.ZipFile(temp, 'w', zipfile.ZIP_DEFLATED)
        try:
            VirtualCoach.__zip_directory(dirpath, zip_file)
        except Exception as e:
            logger.error('The folder %s could not be zipped', dirpath)
            raise e
        zip_file.close()
        content = open(temp, 'rb').read()
        os.remove(temp)
        return content
