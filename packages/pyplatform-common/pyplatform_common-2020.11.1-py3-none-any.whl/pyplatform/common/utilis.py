
import os
import json
import logging
import requests
import jwt
import time


def credhub_get_credentials(output_option='FILE'):
    """Return credhub managed credentials  in pivotal cloud  at runtime from `VCAP_SERVICES` environment variable.

    documentatioin: https://docs.pivotal.io/credhub-service-broker/using.html

    Keyword Arguments:
        output_option {str} -- output format of credentials.
                {'FILE':'downloads credential ``value`` as a temp file, sets credential ``key`` as variable pointing to temp file path'\
                'DICT':'returns credential ``value`` as dict object'}. (default: {'FILE'})

    Recommended credential keys for each platform:
        {'gpc':'GOOGLE_APPLICATION_CREDENTIALS' \
            ,'azure': 'AZURE_CREDENTIALS' \
            , 'pivotal':'PIVOTAL_CREDENTIALS' \
            ,'tableau','TABLEAU_SERVER_CREDENTIALS' }

    Returns:
        {str, dict} -- filepath as str and dict as value of credentials
    """
    service = os.environ.get('VCAP_SERVICES')
    if service:
        env = json.loads(service)
        cred_name = [cred.get('name') for cred in env.get('credhub')]
        logging.debug(f"names of available credentials: {cred_name}")
    else:
        cred_name = None

    if cred_name:
        temp_files = []
        creds = {}
        credhub = [cred.get('credentials') for cred in env.get('credhub')]
        for i, name in enumerate(cred_name):

            key, value = zip(*credhub[i].items())
            key, value = key[0], value[0]

            if output_option != 'DICT':
                if not os.path.exists('temp'):
                    os.mkdir('temp')
                temp_cred = os.path.join(
                    'temp', f'{name}_temp_credentials.json')

                with open(temp_cred, 'w') as file:
                    file.write(value)

                os.environ[key] = temp_cred
                temp_files.append(temp_cred)
            else:
                if isinstance(value, str):
                    try:
                        creds[key] = json.loads(value)
                    except:
                        logging.warning(
                            f"{name} is invalid json, passing on as string")
                        creds[key] = value
                else:
                    creds[key] = value

        if temp_files:
            return temp_files
        else:
            return creds
    else:
        logging.debug(f"no credentails set in credhub")


def gcp_get_auth_header(scope='https://www.googleapis.com/auth/devstorage.read_only', output_option='AUTH_HEADER', credentials_file_path=None):
    """Return OAuth2 Authorization header for google api calls.

    Keyword Arguments:
        scope {str} -- authorization scope (default: {'https://www.googleapis.com/auth/devstorage.read_only'})
            cloud_function_scope='https://www.googleapis.com/auth/cloud-platform' or
            cloud_function_scope = 'https://www.googleapis.com/auth/cloudfunctions'
        output_option {str} -- output format of function (default: {'AUTH_HEADER'})
            other options include {'TOKEN','RESPONSE','JSON'}
        credentials_file_path {str} -- file path of google service account (default: {None})

    Returns:
        {str, requests.response, requests.response.json} -- AUTH_HEADER and TOKEN are str
    """

    if not credentials_file_path:
        logging.debug(
            "credentials file not provided, using env variable GOOGLE_APPLICATION_CREDENTIALS")
        credentials_file_path = os.environ.get(
            'GOOGLE_APPLICATION_CREDENTIALS')
        if not credentials_file_path:
            logging.error("Default credentials not set")
            credentials_file_path = 'no-cred'

    if os.path.isfile(credentials_file_path):
        with open(credentials_file_path) as file:
            credentials = json.loads(file.read())

        client_secret = credentials['private_key']
        client_email = credentials['client_email']
        # "https://oauth2.googleapis.com/token"
        token_uri = credentials['token_uri']

        iat = time.time()
        exp = iat + 3600
        payload = {'iss': client_email,
                   'sub': client_email,
                   'scope': scope,
                   'aud': token_uri,
                   'iat': iat,
                   'exp': exp}
        additional_headers = {'kid': client_secret}
        signed_jwt = jwt.encode(payload, client_secret, headers=additional_headers,
                                algorithm='RS256')
        if output_option == 'JWT':
            return signed_jwt

        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                "assertion": signed_jwt}
        response = requests.request(
            "POST", token_uri, headers=headers, data=data)
        if response.status_code == 200:
            access_token = response.json()['access_token']
            if output_option == 'TOKEN':
                return access_token
            elif output_option == 'RESPONSE':
                return response
            elif output_option == 'JSON':
                return response.json()
            else:
                return f'Bearer {access_token}'
        else:
            logging.error(
                f"access_token request unsuccessfull with status code {response.status_code}")
            return response

    else:
        logging.error(
            "credential file not provided nor env variable GOOGLE_APPLICATION_CREDENTIALS is set to cred path")


def gcs_reader(gcs_uri, auth_header=None, output_option='TEXT'):
    """GET request to Google Cloud Storage api with core Python libraries.

    Arguments:
        gcs_uri {str} -- google cloud storage blob uri e.g. gs://bucketname/foldername/blobname.csv

    Keyword Arguments:
        auth_header {str} -- Bear Authoration token (default: {None})
        output_option {str} -- format of output (default: {'TEXT'})
            other options include {'RESPONSE','CONTENT','JSON','TEXT'}

    Returns:
        {str, requests.response, requests.response.content, requests.response.json, requests.response.text} 
    """
    from urllib.parse import quote_plus
    if not auth_header:
        auth_header = gcp_get_auth_header()  # dependency

    bucket = gcs_uri[5:].split('/')[0]
    blob = quote_plus('/'.join(gcs_uri[5:].split('/')[1:]))

    url = f'https://storage.googleapis.com/storage/v1/b/{bucket}/o/{blob}'

    headers = {
        'Authorization': auth_header,
        'content-type': 'application/json'
    }
    response = requests.get(url, headers=headers, params={'alt': 'media'})
    logging.debug(
        f"response code from {response.url} is {response.status_code}")

    if output_option == 'RESPONSE':
        return response
    elif output_option == 'CONTENT':
        return response.content
    elif output_option == 'JSON':
        return response.json()
    else:
        return response.text


def make_requirements_txt(project_dir='.'):
    """Make requirements.txt file from main.py or module folder.

    Keyword Arguments:
        project_dir {str} -- path to main.py or project folder (default: {'current directory'})
            Note: project folder must end with / (mac/linux) or \ for Windows
    """
    if project_dir == '.':
        project_dir = os.path.curdir
    else:
        project_dir = os.path.dirname(project_dir)
#         os.chdir(script_path)
    return os.system(f"pipreqs {project_dir}")
