from komoot_connector import login_to_komoot, get_all_trails_from_komoot
from pocketbase_connector import login_to_pocketbase
from wanderer_connector import login_to_wanderer
from utils import get_location_from_lat_lon, map_sport_to_category
from pocketbase.client import FileUpload
from dotenv import load_dotenv
import os

load_dotenv()
        
def import_trails_from_komoot_to_wanderer(pb_client, w_auth, trails, connector):
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
    for trail in trails:
        wanderer_category = map_sport_to_category(trail.sport)
        town = get_location_from_lat_lon(trail.start_point.lat, trail.start_point.lon)
        
        # generate GPX track
        trail.generate_gpx_track(authentication=connector.authentication)

        # save GPX track to file
        os.makedirs("gpx_files", exist_ok=True)
        gpx_filename = f"./gpx_files/{trail.name}.gpx"
        with open(gpx_filename, 'w') as gpx_file:
            gpx_file.write(trail.gpx_track.to_xml())

        # if trail has no difficulty, set it to "easy"
        trail_difficulty = "easy"
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
        record = pb_client.collection("trails").create(data)
        print(f"Trail {trail.name} imported to Wanderer with ID {record.collection_id}")
        
        # remove GPX file
        os.remove(gpx_filename)
  
  
if __name__ == "__main__":   
    connector = login_to_komoot()  
    pb_client = login_to_pocketbase()      
    w_auth = login_to_wanderer()
    trails = get_all_trails_from_komoot(connector)
    import_trails_from_komoot_to_wanderer(pb_client, w_auth, trails, connector)




  