# SportEasy Calendar Connector

Generates ICS from SportEasy

## Simple and rapid use

Go to https://sporteasy-calendar-connector.tbmc.ovh

## Add SportEasy events to Google Calendar

1. Click here:

![FromUrl](./docs/fromUrl.png)

2. Paste generated default URL here

![FromUrlPasteHere](./docs/fromUrlPasteUrl.png)

## Installation with Docker

Example [`docker-compose.yml`](./docker-compose.yml)

Application listen on port `5000`.

The same image is available from 2 different registry:

| Host                                                                                                           | Docker image                                     |
|----------------------------------------------------------------------------------------------------------------|--------------------------------------------------|
| [ Github ]( https://github.com/tbmc/sporteasy-calendar-connector/pkgs/container/sporteasy-calendar-connector ) | ghcr.io/tbmc/sporteasy-calendar-connector:latest |
| [ Docker Hub ]( https://hub.docker.com/r/tbmc/sporteasy-calendar-connector )                                   | tbmc/sporteasy-calendar-connector:latest         |

## How to use it

### Populate ``.env``

You need to populate ``.env`` with at least you SportEasy username and password.
You can also add ``team_id`` to only have event of only one team instead of all your teams.

To get all team names and IDs you can use ``list_teams.py`` after populating `username` and `password` in `.env`.

### Encode logins

#### With script

You can use ``env_to_base64.py`` script with `.env` populated.

### Manually

#### Generate logins

Take json and transform it to base64, then url encode it

```json
{
  "username": "...",
  "password": "...",
  "team_id": 123456
}
```

``team_id`` is optional.

## With my server

You can use mine, but at your own risk.

:warning: Data in base64 are not ciphered.

``
https://sporteasy-calendar-connector.tbmc.ovh?data={base64Data}
``

## Info

SportEasy block IPs from server providers, so you should have a domestic IP.

