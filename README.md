## komoot-to-wanderer

A few days ago i discoverd [Wanderer](https://github.com/Flomp/wanderer), a beautiful hiking app that allows you to create and share hiking routes. I wanted to try it out, but i didn't want to create all my routes manually. So i wrote this script to import my routes from [Komoot](https://www.komoot.com/) to Wanderer. Since I couldn't get the implemented API to work, I went the other way and accessed the [Pocketbase](https://github.com/pocketbase/pocketbase) backend directly. It also uploads your recorded GPX tracks and fetches the start location using the [Nominatim](https://github.com/osm-search/Nominatim) API.

## Installation

Make sure you have Python 3 installed on your machine.

Without virtual environment:

```
git clone https://github.com/doen1el/komoot-to-wanderer.git
cd komoot-to-wanderer
pip install -r requirements.txt
```

With virtual environment:

```
git clone https://github.com/doen1el/komoot-to-wanderer.git
cd komoot-to-wanderer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Preparation:

Create a `.env` file in the root directory of the project with the following content:

```
WANDERER_BASE_URL=http://your-wanderer-url
WANDERER_EMAIL=your-wanderer-email
WANDERER_PASSWORD=your-wanderer-password

KOMOOT_EMAIL=your-komoot-email
KOMOOT_PASSWORD=your-komoot-password

POCKETBASE_BASE_URL=your-pocketbase-url
```

Change the values to your own credentials.

## Usage:

```
python3 main.py
```

Due to the request to the nominatim API, the script may take a while to finish. So maybe go for a walk ;)

## Special Thanks to the following projects:

- [Nominatim](https://github.com/osm-search/Nominatim)
- [Wanderer](https://github.com/Flomp/wanderer)
- [Pocketbase Python SDK](https://github.com/vaphes/pocketbase)
- [Kompy](https://github.com/Tsadoq/kompy)
