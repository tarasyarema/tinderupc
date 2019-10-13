## Api reference

### Register: `POST /register`
#### Request
Can be called via form data or JSON body.
The format has to be the following:
```json
{
	"email": "biene@hackupc.com",
	"password": "biene",
	"description": "Hola, m'agrada no dormir!",
	"lang": "Python 3.7"
}
```

#### Returns
A JWT token.
```json
HTTP 200

{
   "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjVkYTI4OTk0NmNkMWNhM2E5MDg4ZDg1NSJ9.ohkLJrptxT0F4wuQekOQEK-qpxNHnrA-jVTwZ4psx74"
}
```

### Login: `POST /login`
#### Request
Can be called via form data or JSON body.
The format has to be the following:
```json
{
	"email": "biene@hackupc.com",
	"password": "biene"
}
```

#### Returns
A JWT token.
```json
HTTP 200

{
   "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6IjVkYTI4OTk0NmNkMWNhM2E5MDg4ZDg1NSJ9.ohkLJrptxT0F4wuQekOQEK-qpxNHnrA-jVTwZ4psx74"
}
```

### Get stack: `GET /`
#### Request
The token as a `Authorization: Bearer {token}` header.

#### Returns
Returns JSON
```json
HTTP 200

{
   "data": [
      {
         "id": "5da25e5286dc7e9c3be99a0d",
         "data": {
            "lang": "C",
            "desccription": "I like maths!"
         }
      },
      {
         "id": "5da25e5286dc7e9c3be99a0d",
         "data": {
            "lang": "Python",
            "desccription": "I like to suck :3"
         }
      }
   ]
}
```

### Vote: `POST /vote`
#### Request
Can be called via form data or JSON body.
The format has to be the following:
```json
{
	"id_a": "5da25e5286dc7e9c3be99a0d",
	"id_b": "5da26d9687f808f820d54233",
	"win": false
}
```

The parameters mean:
1. `id_a`: User A id.
2. `id_b`: User B id.
3. `win`: True if the selected is id_a, False if it's id_b. 


#### Returns
```json
HTTP 200

{
   "message": "user relations updated"
}
```

### Get ranking: `GET /ranking`
#### Request
The token as a `Authorization: Bearer {token}` header.

#### Returns
Returns JSON with an array (actual max 5 elements, may be changed xd).
```json
HTTP 200

{
   "data": [
      {
         "elo": 1534.137483083232,
         "id": "5da23afa05650a08e4ca6a8f"
      },
      {
         "elo": 1532.8705963547923,
         "id": "5da26d9687f808f820d54233"
      },
      {
         "elo": 1528.0781000835332,
         "id": "5da25e5286dc7e9c3be99a0d"
      },
      {
         "elo": 1465.0496502835474,
         "id": "5da25857e57c8c0839a12bea"
      },
      {
         "elo": 1434.9030321116102,
         "id": "5da25e8e5dd47b259e2ac2e3"
      }
   ]
}
```
# Run
Execute `startDB.sh`, `build.sh` and `run.sh`.
You will need a `.env` file with the following envars:
```
SECRET=
MONGO_HOST=
MONGO_PORT=
MONGO_INITDB_ROOT_USERNAME=
MONGO_INITDB_ROOT_PASSWORD=
```
