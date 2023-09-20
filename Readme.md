# SportEasy Calendar Connector

Generates ics from SportEasy

## How to use it

### With script

Use ``env_to_base64.py`` script with `.env` populated.

### Manually

#### Generate logins
Take json and transform it to base64, then url encode it
```json
{
    "username": "...",
    "password": "...",
    "team_id": ...
}
```

``team_id`` is optional. 

#### Url

``
https://sporteasy-converter.***REMOVED***?data={base64Data}
``

