from helper.pocketbase_connector import login_to_pocketbase, get_all_trails_from_wanderer
from helper.komoot_connector import login_to_komoot, get_all_trails_from_komoot
from helper.wanderer_connector import login_to_wanderer
from helper.utils import get_location_from_lat_lon, map_sport_to_category
from pocketbase.client import FileUpload
from dotenv import load_dotenv
import schedule
import time
import os

load_dotenv()

def print_env_variables():
    """
    Prints all environment variables from the .env file.
    """
    print('Environment Variables:')
    print(f"WANDERER_BASE_URL: {os.getenv('WANDERER_BASE_URL')}")
    print(f"WANDERER_EMAIL: {os.getenv('WANDERER_EMAIL')}")
    print(f"WANDERER_PASSWORD: {os.getenv('WANDERER_PASSWORD')}")
    print(f"KOMOOT_EMAIL: {os.getenv('KOMOOT_EMAIL')}")
    print(f"KOMOOT_PASSWORD: {os.getenv('KOMOOT_PASSWORD')}")
    print(f"POCKETBASE_BASE_URL: {os.getenv('POCKETBASE_BASE_URL')}")
    print(f"SCHEDULE_TIME: {os.getenv('SCHEDULE_TIME')}")
        
def import_trails_from_komoot_to_wanderer(pb_client, w_auth, komoot_trails, wanderer_trails, connector):
    """
    Imports trails from Komoot to Wanderer.
    This function takes a list of trails from Komoot, generates GPX tracks for each trail,
    and imports them into the Wanderer platform.
    Args:
        pb_client (PocketBaseClient): The PocketBase client used to interact with the Wanderer API.
        w_auth (dict): The authentication information for the Wanderer API.
        trails (list): A list of trail objects to be imported.
        connector (Connector): The connector object used for authentication and generating GPX tracks.
    Returns:
        None
    """
    for trail in komoot_trails:
        
        # check if trail already exists in Wanderer
        if trail.name in wanderer_trails:
            print(f"Trail {trail.name} already exists in Wanderer")
            continue
        
        wanderer_category = map_sport_to_category(trail.sport)
        town = get_location_from_lat_lon(trail.start_point.lat, trail.start_point.lon)
        
        # generate GPX track
        trail.generate_gpx_track(authentication=connector.authentication)

        # save GPX track to file
        os.makedirs('gpx_files', exist_ok=True)
        gpx_filename = f"./gpx_files/{trail.name}.gpx"
        with open(gpx_filename, 'w') as gpx_file:
            gpx_file.write(trail.gpx_track.to_xml())

        # if trail has no difficulty, set it to "easy"
        trail_difficulty = 'easy'
        if trail.difficulty != None:
            trail_difficulty = trail.difficulty.grade
    
        # track data to be imported
        data = {
            "name": trail.name,
            "public": False,
            "category": wanderer_category,
            "date": trail.start_date.isoformat(),
            "description": "",
            "difficulty": trail_difficulty,
            "distance": trail.distance,
            "duration": trail.total_duration / 60,
            "elevation_gain": trail.elevation_up,
            "elevation_loss": trail.elevation_down,
            "lat": trail.start_point.lat if trail.start_point.lat else 0,
            "location": town if town else "Unknown",
            "lon": trail.start_point.lon if trail.start_point.lon else 0,
            "thumbnail": 0,
            "author": w_auth['record']['id'],
            "gpx": FileUpload((gpx_filename, open(gpx_filename, "rb"))),
        }

        # create trail in Wanderer
        record = pb_client.collection('trails').create(data)
        print(f"Trail {trail.name} imported to Wanderer with ID {record.collection_id}")
        
        # remove GPX file
        os.remove(gpx_filename)
   
def main():  
    """
    Main function to handle the process of importing trails from Komoot to Wanderer.
    This function performs the following steps:
    1. Logs into Komoot and retrieves a connector object.
    2. Logs into PocketBase and retrieves a client object.
    3. Logs into Wanderer and retrieves an authentication object.
    4. Retrieves all trails from Komoot using the connector.
    5. Retrieves all trails from Wanderer using the PocketBase client.
    6. Imports trails from Komoot to Wanderer using the provided authentication and connector objects.
    Returns:
        None
    """
    connector = login_to_komoot()  
    pb_client = login_to_pocketbase()      
    w_auth = login_to_wanderer()
    komoot_trails = get_all_trails_from_komoot(connector)
    wanderer_trails = get_all_trails_from_wanderer(pb_client)
    import_trails_from_komoot_to_wanderer(pb_client, w_auth, komoot_trails, wanderer_trails, connector)

if __name__ == "__main__":    
    # Print environment variables at the start
    print_env_variables()

    # Schedule the main function to run daily at the specified time
    schedule.every().day.at(os.getenv('SCHEDULE_TIME')).do(main)

    # Wait for the scheduled function to run
    while 1:
        schedule.run_pending()
        time.sleep(1)