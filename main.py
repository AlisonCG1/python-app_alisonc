import os
from dotenv import load_dotenv
import hvac

load_dotenv()

VAULT_URL = os.getenv("VAULT_PATH")
USERNAME = os.getenv("VAULT_USER")
PASSWORD = os.getenv("VAULT_PASSWORD")

def get_vault_token_userpass(username, password):
    """
    Authenticate with Vault using userpass authentication method and return the client.
    """
    try:
        client = hvac.Client(url=VAULT_URL)
        login_response = client.auth.userpass.login(
            username=username, password=password
        )
        if client.is_authenticated():
            print("Successfully authenticated with Vault.")
            return client
        else:
            print("Authentication failed.")
            return None
    except Exception as e:
        print(f"Authentication error: {e}")
        return None

def read_secret(client, mount_point, path):
    """Read a secret from Vault."""
    if not client:
        return None
    try:

        secret_response = client.secrets.kv.v2.read_secret_version(
            mount_point=mount_point, path=path
        )
        return secret_response['data']['data']
    except Exception as e:
        print(f"Error reading KV v2 secret: {e}")
        try:

            secret_response = client.secrets.kv.v1.read_secret(
                mount_point=mount_point, path=path
            )
            return secret_response['data']
        except Exception as e:
            print(f"Error reading KV v1 secret: {e}")
            return None

if __name__ == "__main__":
    if VAULT_URL and USERNAME and PASSWORD:
        client = get_vault_token_userpass(USERNAME, PASSWORD)
        if client:
            secret_data = read_secret(client, "kv", "mysecret2_AC")
            if secret_data:
                print(f"Secret: {secret_data}")
            else:
                print("Failed to retrieve secret.")
        else:
            print("Failed to retrieve client.")
    else:
        print("Missing environment variables: VAULT_PATH, VAULT_USER, or VAULT_PASSWORD.")