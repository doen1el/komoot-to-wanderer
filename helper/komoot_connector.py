from kompy import KomootConnector
import os

def login_to_komoot():
    """
    Logs in to the Komoot service using credentials stored in environment variables.
    This function retrieves the Komoot email and password from the environment variables
    'KOMOOT_EMAIL' and 'KOMOOT_PASSWORD', respectively, and uses them to create an instance
    of the KomootConnector class.
    Returns:
        KomootConnector: An instance of the KomootConnector class initialized with the provided credentials.
    """
    connector = KomootConnector(password=os.getenv('KOMOOT_PASSWORD'), email=os.getenv('KOMOOT_EMAIL'))
    print('Authenticated with Komoot')
    return connector

def get_all_trails_from_komoot(connector):
    """
    Retrieve all trails from the Komoot service using the provided connector.
    Args:
        connector: An instance of a connector class that interfaces with the Komoot API.
    Returns:
        A list of tours retrieved from the Komoot service.
    """
    print('Retrieving trails from Komoot')
    return connector.get_tours(user_identifier=None)