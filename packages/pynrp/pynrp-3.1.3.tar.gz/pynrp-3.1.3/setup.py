'''setup.py'''

# pylint: disable=F0401,E0611,W0622,E0012,W0142,W0402

from builtins import str
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

from optparse import Option  # pylint:disable=deprecated-module
import pip
import pathlib
import pynrp

README = (pathlib.Path(__file__).parent / "README.txt").read_text()

options = Option('--workaround')
options.skip_requirements_regex = None
reqs_file = './requirements.txt'

pip_version_major = int(pip.__version__.split('.')[0])
# Hack for old pip versions
if pip_version_major == 1:
    # Versions 1.x rely on pip.req.parse_requirements
    # but don't require a "session" parameter
    from pip.req import parse_requirements # pylint:disable=no-name-in-module, import-error
    install_reqs = parse_requirements(reqs_file, options=options)
    reqs = [str(ir.req) for ir in install_reqs]
elif 10 > pip_version_major > 1:
    # Versions greater than 1.x but smaller than 10.x rely on pip.req.parse_requirements
    # and requires a "session" parameter
    from pip.req import parse_requirements # pylint:disable=no-name-in-module, import-error
    from pip.download import PipSession  # pylint:disable=no-name-in-module, import-error
    options.isolated_mode = False
    install_reqs = parse_requirements(  # pylint:disable=unexpected-keyword-arg
        reqs_file,
        session=PipSession,
        options=options
    )
    reqs = [str(ir.req) for ir in install_reqs]
elif pip_version_major >= 10:
    # Versions greater or equal to 10.x don't rely on pip.req.parse_requirements
    install_reqs = list(val.strip() for val in open(reqs_file))
    reqs = install_reqs

config = {
    'description': 'Python interface to the Neurorobotics Platform (NRP)',
    'long_description': README,
    'long_description_content_type': 'text/markdown',
    'author': 'HBP Neurorobotics',
    'url': 'http://neurorobotics.net',
    'author_email': 'neurorobotics@humanbrainproject.eu',
    'version': pynrp.__version__,
    'install_requires': reqs,
    'packages': ['pynrp'],
    'package_data': {
        'pynrp': ['config.json']
    },
    'classifiers': ['Programming Language :: Python :: 3.8'],
    'scripts': [],
    'name': 'pynrp',
    'include_package_data': True,
}

setup(**config)
