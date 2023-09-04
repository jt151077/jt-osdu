import requests
import json
import subprocess
import urllib
import urllib.request


def getConfig(url):
  urllib.request.urlretrieve(url, "jtosdu/config.json")
  
  parsed_json = {}
  with open('jtosdu/config.json') as user_file:
    parsed_json = json.load(user_file)

  return parsed_json


def getHeaders(bearer, data_partition_id):
  headers = {
    "data-partition-id": data_partition_id,
    "Authorization": bearer
  }
  return headers


def get_groups_success_scenario(headers, baseurl):
  response = requests.get('https://{}/api/entitlements/v2/groups'.format(baseurl), headers=headers)
  return response.json()



def auth_gcp_authorisation_code_flow(client_id, client_secret, output, scope, grant_type, data_partition_id):
  print("Go to this URL in a browser:: https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?access_type=offline&prompt=consent&response_type=code&client_id={}&scope={}&redirect_uri=https%3A%2F%2Foauth.pstmn.io%2Fv1%2Fbrowser-callback".format(client_id, scope))
  auth_code=input("Enter your authorization code: ")
  
  data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': grant_type,
    'access_type': 'offline',
    'code': urllib.parse.unquote(auth_code),
    'redirect_uri': 'https://oauth.pstmn.io/v1/browser-callback'
  }

  gcp_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  response = requests.post('https://oauth2.googleapis.com/token', data, headers=gcp_headers)
  
  print ("Login to GCP successful")

  return getHeaders(("Bearer {}").format(response.json()['access_token']), data_partition_id)



def auth_azr_authorisation_code_flow(client_id, client_secret, output, scope, grant_type, data_partition_id, tenant_id):
  print("Go to this URL in a browser::https://login.microsoftonline.com/{}/oauth2/v2.0/authorize?access_type=offline&prompt=consent&response_type=code&client_id={}&scope={}&redirect_uri=https%3A%2F%2Foauth.pstmn.io%2Fv1%2Fbrowser-callback".format(tenant_id, client_id, scope))
  auth_code=input("Enter your authorization code: ")
  
  data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'grant_type': 'authorization_code',
    'access_type': 'offline',
    'code': urllib.parse.unquote(auth_code),
    'redirect_uri': 'https://oauth.pstmn.io/v1/browser-callback'
  }

  azr_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  response = requests.post('https://login.microsoftonline.com/{}/oauth2/v2.0/token'.format(tenant_id), data, headers=azr_headers)
  
  print ("Login to AZR successful")

  return getHeaders(("Bearer {}").format(response.json()['access_token']), data_partition_id)



def auth_azr_credential_flow(client_id, client_secret, scope, grant_type, data_partition_id, tenant_id):
  data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope,
    'grant_type': grant_type
  }

  azr_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  response = requests.post('https://login.microsoftonline.com/{}/oauth2/v2.0/token'.format(tenant_id), data, headers=azr_headers)
  
  print ("Login to AZR successful")

  return getHeaders(("Bearer {}").format(response.json()['access_token']), data_partition_id)

