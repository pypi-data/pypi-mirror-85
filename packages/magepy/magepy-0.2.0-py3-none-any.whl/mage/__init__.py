import botocore
import getpass
import os
import sys

from dotenv import load_dotenv
from sgqlc.endpoint.http import HTTPEndpoint
from warrant.aws_srp import AWSSRP

from os.path import expanduser

import logging

#logging.basicConfig()
logger = logging.getLogger(__name__) #: logging.Logger: The MAGE Logger
logger.setLevel(logging.INFO)

auto_page = False #: bool: Iterators should iterate through all data, fetching more from the server as needed


def _get_credentials():
    username = input('Username: ')
    password = getpass.getpass(prompt='Password: ')
    return username, password

def connect(envfile_path = None):
    """
    Connects to the MAGE server.  The connection details may be passed in as an argument.  Additional locations checked for the information include: ~/.env and ./.env

    Args:
        envfile_path (str, optional): Location of file that contains the connection parameters.

    Returns:
        bool: True on success, False on failure
    """
    global client_id
    global endpoint

    username = None
    password = None

    home_env = expanduser("~/.env")
    if envfile_path and not os.path.isfile(envfile_path):
        print('[-] Error locating %s' % envfile_path)

    for f in [home_env, '.env', envfile_path]:
        if f and os.path.isfile(f):
            load_dotenv(f)
            username = os.getenv('COGNITO_USERNAME')
            password = os.getenv('COGNITO_PASSWORD')

    gql_url = os.getenv('GQL_URL')
    pool_id = os.getenv('POOL_ID')
    client_id = os.getenv('CLIENT_ID')

    if not all([gql_url, pool_id, client_id]):
        print('[-] You must supply a GQL_URL, POOL_ID, and CLIENT_ID in your environment')
        print("""[!] You can create a .env file with these values at:
    * ./.env
    * in %s
    * the location passed into the connect function""" % home_env)
        return False

    if not username or not password:
        print('[!] Could not load Cognito credentials from .env file')
        username, password = _get_credentials()


    ##########################

    print('[*] Authenticating')
    try:
        u = AWSSRP(
            username=username,
            password=password,
            pool_id=pool_id,
            client_id=client_id
        )
    except botocore.exceptions.NoRegionError:
        os.environ['AWS_DEFAULT_REGION'] = 'us-east-1'
        u = AWSSRP(
            username=username,
            password=password,
            pool_id=pool_id,
            client_id=client_id
        )

    tokens = u.authenticate_user()
    auth = tokens['AuthenticationResult']['AccessToken']
    headers = {'Authorization': auth, 'Content-Type': 'application/json'}

    endpoint = HTTPEndpoint(gql_url, headers, None)

    print('[*] Retrieving client id')
    client_id = Client.select('id').list()[0].id

    return (client_id is not None and endpoint is not None)


client_id = None
endpoint = None

from .api_resources import *
from .query import *
