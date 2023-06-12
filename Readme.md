# SportEasy Calendar Connector

Generates ics from SportEasy

## How to use it

### With script

Use ``env_to_base64.py`` script with `.env` populated.

### Manually

#### Generate logins
Take json and transform it to base64 without last `=`
```json
{
    "username": "...",
    "password": "..."
}
```

#### Url
``
https://sporteasy-converter.***REMOVED***?data={base64Data}
``

