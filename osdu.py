import requests
import json
import subprocess

def getHeaders(bearer, data_partition_id):
  headers = {
    "data-partition-id": data_partition_id,
    "Authorization": bearer
  }
  return headers


def get_groups_success_scenario(headers, baseurl):
  response = requests.get('https://{}/api/entitlements/v2/groups'.format(baseurl), headers=headers)
  return response.json()


def formatx(i, key, j, k, r):
  val=r[i].split(": ")[1][1-j:-2+j+k]
  return key+": "+val


def auth_gcp_authorisation_code_flow(client_id, client_secret, output, scope, grant_type, data_partition_id):
  print("Go to this URL in a browser:: https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?access_type=offline&prompt=consent&response_type=code&client_id={}&scope={}&redirect_uri=https%3A%2F%2Foauth.pstmn.io%2Fv1%2Fbrowser-callback".format(client_id, scope))
  auth_code=input("Enter your authorization code: ")
  output.clear()
  response = subprocess.check_output("curl -d client_id={} -d client_secret={} -d grant_type={} -d redirect_uri=https%3A%2F%2Foauth.pstmn.io%2Fv1%2Fbrowser-callback -d code={} https://accounts.google.com/o/oauth2/token".format(client_id, client_secret, grant_type, auth_code), shell=True).decode().split("\n")[1:6]
  access_token, expires_in, refresh_token, scope, token_type = formatx(0, "access_token", 0, 0, response), formatx(1, "expires_in", 1, 0, response), formatx(2, "refresh_token", 0, 0, response), formatx(3, "scope", 0, 0, response), formatx(4, "token_type", 0, 1, response)
  return getHeaders(("Bearer {}").format((access_token.split("access_token: "))[1]), data_partition_id)

  
def auth_azr_authorisation_code_flow(client_id, client_secret, output, scope, grant_type, data_partition_id):
  print("Go to this URL in a browser::https://login.microsoftonline.com/3aa4a235-b6e2-48d5-9195-7fcf05b459b0/oauth2/v2.0/authorize?access_type=offline&prompt=consent&response_type=code&client_id={}&scope={}&redirect_uri=https%3A%2F%2Foauth.pstmn.io%2Fv1%2Fbrowser-callback".format(client_id, scope))
  auth_code=input("Enter your authorization code: ")
  output.clear()
  response = subprocess.check_output("curl -d client_id={} -d client_secret={} -d grant_type={} -d redirect_uri=https%3A%2F%2Foauth.pstmn.io%2Fv1%2Fbrowser-callback -d code={} https://login.microsoftonline.com/3aa4a235-b6e2-48d5-9195-7fcf05b459b0/oauth2/v2.0/token".format(client_id, client_secret, grant_type, auth_code), shell=True).decode().split("\n")[1:6]
  access_token, expires_in, refresh_token, scope, token_type = formatx(0, "access_token", 0, 0, response), formatx(1, "expires_in", 1, 0, response), formatx(2, "refresh_token", 0, 0, response), formatx(3, "scope", 0, 0, response), formatx(4, "token_type", 0, 1, response)
  return getHeaders(("Bearer {}").format((access_token.split("access_token: "))[1]), data_partition_id)


def auth_azr_credential_flow(client_id, client_secret, scope, grant_type, data_partition_id):
  data = {
    'client_id': client_id,
    'client_secret': client_secret,
    'scope': scope,
    'grant_type': grant_type
  }

  azr_headers = {'Content-Type': 'application/x-www-form-urlencoded'}
  response = requests.post('https://login.microsoftonline.com/3aa4a235-b6e2-48d5-9195-7fcf05b459b0/oauth2/v2.0/token', data, headers=azr_headers)
  
  return getHeaders(("Bearer {}").format(response.json()['access_token']), data_partition_id)

