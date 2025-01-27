import requests

def get_location_from_lat_lon(lat, lon):
    """
    Retrieves the town name for a given latitude and longitude using the Nominatim API from OpenStreetMap.
    Args:
        lat (float): The latitude of the location.
        lon (float): The longitude of the location.
    Returns:
        str: The name of the town corresponding to the given latitude and longitude.
    Raises:
        HTTPError: If the HTTP request returned an unsuccessful status code.
    """
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:134.0) Gecko/20100101 Firefox/134.0"
    }
    url = f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json"
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json().get("address").get("town")
    else:
        response.raise_for_status()
        
def map_sport_to_category(komoot_sport):
    """
    Maps a given Komoot sport type to a corresponding Wanderer category ID.
    Args:
        komoot_sport (str): The sport type from Komoot.
    Returns:
        str: The corresponding Wanderer category ID. Defaults to the ID for "Walking" if the sport type is not found.
    Komoot to Wanderer mapping:
        - "hike", "mountaineering", "jogging", "nordicwalking", "snowshoe", "other" -> "03i1quibm01ixaq" (Walking)
        - "racebike", "e_racebike", "touringbicycle", "e_touringbicycle", "mtb", "e_mtb", "mtb_easy", "e_mtb_easy", "mtb_advanced", "e_mtb_advanced", "downhillbike", "skaten", "unicycle", "citybike" -> "7zab78v44pl8s6w" (Biking)
        - "climbing" -> "a5wgjqjah2lr67z" (Climbing)
        - "nordic", "skialpin", "skitour", "sled", "snowboard" -> "S34ssopmsbhg5ibg" (Skiing)
    """
    
    komoot_to_wanderer = {
        "hike": "03i1quibm01ixaq",  # Walking
        "mountaineering": "03i1quibm01ixaq",  # Walking
        "racebike": "7zab78v44pl8s6w",  # Biking
        "e_racebike": "7zab78v44pl8s6w",  # Biking
        "touringbicycle": "7zab78v44pl8s6w",  # Biking
        "e_touringbicycle": "7zab78v44pl8s6w",  # Biking
        "mtb": "7zab78v44pl8s6w",  # Biking
        "e_mtb": "7zab78v44pl8s6w",  # Biking
        "mtb_easy": "7zab78v44pl8s6w",  # Biking
        "e_mtb_easy": "7zab78v44pl8s6w",  # Biking
        "mtb_advanced": "7zab78v44pl8s6w",  # Biking
        "e_mtb_advanced": "7zab78v44pl8s6w",  # Biking
        "jogging": "03i1quibm01ixaq",  # Walking
        "climbing": "a5wgjqjah2lr67z",  # Climbing
        "downhillbike": "7zab78v44pl8s6w",  # Biking
        "nordic": "S34ssopmsbhg5ibg",  # Skiing
        "nordicwalking": "03i1quibm01ixaq",  # Walking
        "skaten": "7zab78v44pl8s6w",  # Biking
        "skialpin": "S34ssopmsbhg5ibg",  # Skiing
        "skitour": "S34ssopmsbhg5ibg",  # Skiing
        "sled": "S34ssopmsbhg5ibg",  # Skiing
        "snowboard": "S34ssopmsbhg5ibg",  # Skiing
        "snowshoe": "03i1quibm01ixaq",  # Walking
        "unicycle": "7zab78v44pl8s6w",  # Biking
        "citybike": "7zab78v44pl8s6w",  # Biking
        "other": "03i1quibm01ixaq"  # Walking
    }
    
    return komoot_to_wanderer.get(komoot_sport, "03i1quibm01ixaq")  # Default to Walking if not found