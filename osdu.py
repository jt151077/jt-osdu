import requests
import json
import subprocess

headers={}

def setheaders(bearer):
  headers = {
    "data-partition-id": "odesprod",
    "Authorization": bearer
  }

def get_groups_success_scenario():
  response = requests.get('https://preship.gcp.gnrg-osdu.projects.epam.com/api/entitlements/v2/groups', headers=headers)
  return json.dumps(response.json())


def formatx(i, key, j, k, r):
  val=r[i].split(": ")[1][1-j:-2+j+k]
  return key+": "+val

def authorize(client_id, client_secret, output):
  print("Go to this URL in a browser:: https://accounts.google.com/o/oauth2/auth/oauthchooseaccount?access_type=offline&prompt=consent&response_type=code&client_id=605457357143-6h6uqunq67f53m9jeibn38gupd27bsfb.apps.googleusercontent.com&scope=email%20openid%20profile&redirect_uri=https%3A%2F%2Foauth.pstmn.io%2Fv1%2Fbrowser-callback".format(client_id))
  auth_code=input("Enter your authorization code: ")
  output.clear()
  response = subprocess.check_output("curl -d client_id={} -d client_secret={} -d grant_type=authorization_code -d redirect_uri=https%3A%2F%2Foauth.pstmn.io%2Fv1%2Fbrowser-callback -d code={} https://accounts.google.com/o/oauth2/token".format(client_id, client_secret, auth_code), shell=True).decode().split("\n")[1:6]
  access_token, expires_in, refresh_token, scope, token_type = formatx(0, "access_token", 0, 0, response), formatx(1, "expires_in", 1, 0, response), formatx(2, "refresh_token", 0, 0, response), formatx(3, "scope", 0, 0, response), formatx(4, "token_type", 0, 1, response)
  setHeaders("Bearer {}").format((access_token.split("access_token: "))[1]))
  return "Authentication successful"
