[![Github Container Pulls](https://img.shields.io/badge/Github%20Container%20Pulls-1.2K-blue
)](https://github.com/tbmc/sporteasy-calendar-connector/pkgs/container/sporteasy-calendar-connector)
[![Docker Pulls](https://img.shields.io/docker/pulls/tbmc/sporteasy-calendar-connector)](https://hub.docker.com/r/tbmc/sporteasy-calendar-connector)

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

:warning: Do not forget to add populate `SERVER_PRIVATE_KEY` in `.env`. It is now required to encrypted data in links.

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

:warning: Data are encrypted but server still can decrypt it

``
https://sporteasy-calendar-connector.tbmc.ovh/api?data={base64Data}
``

You can add a parameter `disable_save_login` to disable saving of logins and password, but it deactivates links in event description to set present or absent. Without saving logins, it can not connect to SportEasy servers.

``
https://sporteasy-calendar-connector.tbmc.ovh/api?data={base64Data}&disable_save_login=True
``

## Info

SportEasy block IPs from server providers, so you should have a domestic IP.
