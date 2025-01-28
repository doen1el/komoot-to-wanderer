## komoot-to-wanderer

A few days ago i discoverd [Wanderer](https://github.com/Flomp/wanderer), a beautiful hiking app that allows you to create and share hiking routes. I wanted to try it out, but i didn't want to create all my routes manually. So i wrote this script to import my routes from [Komoot](https://www.komoot.com/) to Wanderer. Since I couldn't get the implemented API to work, I went the other way and accessed the [Pocketbase](https://github.com/pocketbase/pocketbase) backend directly. It also uploads your recorded GPX tracks and fetches the start location using the [Nominatim](https://github.com/osm-search/Nominatim) API.

## Installation and Usage

Make sure you have [docker](https://www.docker.com/) installed and running on your machine.

### Clone the repository:

```
git clone https://github.com/doen1el/komoot-to-wanderer.git
cd komoot-to-wanderer
```

### Build the docker image:

```
docker build -t komoot-to-wanderer .
```

### Edite the `docker-compose.yml` file:

```
services:
  komoot-to-wanderer:
    image: komoot-to-wanderer
    container_name: komoot-to-wanderer
    restart: unless-stopped
    environment:
      - WANDERER_BASE_URL=http://your-wanderer-url
      - WANDERER_EMAIL=your-wanderer-email
      - WANDERER_PASSWORD=your-wanderer-password
      - KOMOOT_EMAIL=your-komoot-email
      - KOMOOT_PASSWORD=your-komoot-password
      - POCKETBASE_BASE_URL=your-pocketbase-url
      - SCHEDULE_TIME=00:30:00 # e.g. every day at 00:30
```

| Variable            | Description                         |
| ------------------- | ----------------------------------- |
| WANDERER_BASE_URL   | The base url of the Wanderer API    |
| WANDERER_EMAIL      | Your Wanderer email                 |
| WANDERER_PASSWORD   | Your Wanderer password              |
| KOMOOT_EMAIL        | Your Komoot email                   |
| KOMOOT_PASSWORD     | Your Komoot password                |
| POCKETBASE_BASE_URL | The base url of the Pocketbase API  |
| SCHEDULE_TIME       | The time when the script should run |

### Run the container:

```
docker compose up -d
```

### You can also run the script manually:

```
docker exec -it komoot-to-wanderer python3 main.py
```

Due to the request to the nominatim API, the script may take a while to finish. So maybe go for a walk ;)

## Special Thanks to the following projects:

- [Nominatim](https://github.com/osm-search/Nominatim)
- [Wanderer](https://github.com/Flomp/wanderer)
- [Pocketbase Python SDK](https://github.com/vaphes/pocketbase)
- [Kompy](https://github.com/Tsadoq/kompy)
