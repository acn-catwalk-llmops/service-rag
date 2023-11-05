from base64 import b64encode
import os
import json
import argparse
import requests
from nacl import encoding, public
from dotenv import load_dotenv


parser = argparse.ArgumentParser()
parser.add_argument(
    "envfile",
    nargs="?",
    help="The .env file to be used as source to create GitHub environment",
    type=str,
    default="./env/.env",
)
args = parser.parse_args()

ENV_FILE_PATH = args.envfile

# for now only requiring REGISTRY_TOKEN from env file
load_dotenv(ENV_FILE_PATH)

GITHUB_TOKEN = os.environ["REGISTRY_TOKEN"]
REPOSITORY_ID = "acn-catwalk-llmops/service-rag"
ENVIRONMENT_NAME = "dev"

BASE_URL = f"https://api.github.com/repos/{REPOSITORY_ID}"

headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}


def encrypt(public_key: str, secret_value: str) -> str:
    """Encrypt a Unicode string using the public key."""
    public_key = public.PublicKey(public_key.encode("utf-8"), encoding.Base64Encoder())
    sealed_box = public.SealedBox(public_key)
    encrypted = sealed_box.encrypt(secret_value.encode("utf-8"))
    return b64encode(encrypted).decode("utf-8")


def get_public_key():
    keyurl = f"{BASE_URL}/environments/{ENVIRONMENT_NAME}/secrets/public-key"

    response = requests.request("GET", keyurl, headers=headers, timeout=5)
    print(response)
    data = json.loads(response.text)
    return data["key"], data["key_id"]


def create_environment():
    url = f"{BASE_URL}/environments/{ENVIRONMENT_NAME}"
    payload = {}

    response = requests.request("PUT", url, headers=headers, data=payload, timeout=5)

    if response.status_code == 201:
        print(f"Environment '{ENVIRONMENT_NAME}' created successfully.")
    else:
        print(f"Failed to create environment. Status code: {response.status_code}")
        print(response.text)


# Loading all values as secrets, because why not.
def create_environment_secrets_from_env_file(public_key, public_key_id):
    secrets = {}
    with open(ENV_FILE_PATH, "r") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            key, value = line.split("=", 1)
            secrets[key] = value

    url = f"{BASE_URL}/environments/{ENVIRONMENT_NAME}/secrets"
    for key, value in secrets.items():
        value_encrypted = encrypt(public_key, value)
        data = {"encrypted_value": value_encrypted, "key_id": public_key_id}
        response = requests.put(url + "/" + key, json=data, headers=headers, timeout=5)

        print(
            f"Secret '{key}' in environment '{ENVIRONMENT_NAME}'"
            + f" - status: {response.status_code} - response: {response.text}"
        )


# This script creates the GitHub Environment and Environment Secrets
# needed for the repository's CI/CD.
if __name__ == "__main__":
    create_environment()
    public_key, public_key_id = get_public_key()
    create_environment_secrets_from_env_file(public_key, public_key_id)
