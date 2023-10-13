# Python lib to authenticate with GitHub API using a GitHub App

import jwt
import requests
import time
import os

from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()
APP_ID = os.environ['APP_ID']
INSTALLATION_ID = os.environ['INSTALLATION_ID']
CERTIFICATE = os.environ['CERTIFICATE']


# Helper function to create a JWT
def create_jwt():
    # Open PEM
    with open(CERTIFICATE, 'rb') as pem_file:
        signing_key = jwt.jwk_from_pem(pem_file.read())

        payload = {
            # Issued at time
            'iat': int(time.time()),
            # JWT expiration time (10 minutes maximum)
            'exp': int(time.time()) + 600,
            # GitHub App's identifier
            'iss': APP_ID
        }

        # Create JWT
        jwt_instance = jwt.JWT()
        return jwt_instance.encode(payload, signing_key, alg='RS256')


def get_access_token():
    # Create the JWT for github app authentication
    jwt = create_jwt()

    # Create the headers
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {jwt}",
        "User-Agent": "my-github-app",
        "X-GitHub-Api-Version": "2022-11-28",
    }

    # POST request to get the access token
    r = requests.post(f"https://api.github.com/app/installations/{INSTALLATION_ID}/access_tokens", headers=headers)

    # Return the access token
    return r.json()['token']

if __name__ == '__main__':
    print(get_access_token())
