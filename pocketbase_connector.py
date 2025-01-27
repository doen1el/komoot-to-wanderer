from pocketbase import PocketBase
import os

def login_to_pocketbase():
    """
    Authenticates with PocketBase using environment variables for credentials.
    This function initializes a PocketBase client using the base URL from the 
    environment variable 'POCKETBASE_BASE_URL'. It then attempts to authenticate 
    a user with the email and password provided by the environment variables 
    'WANDERER_EMAIL' and 'WANDERER_PASSWORD'. If authentication fails, an 
    exception is raised.
    Returns:
        PocketBase: An authenticated PocketBase client instance.
    Raises:
        Exception: If authentication with PocketBase fails.
    """
    client = PocketBase(os.getenv("POCKETBASE_BASE_URL"))
    user_data = client.collection("users").auth_with_password(os.getenv("WANDERER_EMAIL"), os.getenv("WANDERER_PASSWORD"))
    if not user_data.is_valid:
        raise Exception("Could not authenticate with PocketBase")
    
    print("Authenticated with PocketBase")
    return client