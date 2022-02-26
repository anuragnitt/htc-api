# **Vortex Hunt The Code 2022 - API**

Previosuly users were provided the files which was risky since users can resort to malpractices such as decompilation and bruteforcing to get the actual algorithm.

This API is used to execute those binary files remotely. The users now provide inputs through `input.py` for a particular question and the input/output exachange is carried out via HTTP requests.

Moreover there is IP based rate limiting to prevent users from bruteforcing the endpoint.

## Setup instructions

* Copy the following files:
    - `assets/config.json.example` to `assets/config.json`
    - `assets/error.log.example` to `assets/error.log`
    - `.env.example` to `.env`

* Mention `question_name: executable_name` settings in `assets/config.json`.

* Fill up the following values in `.env`:
    - `HTC_USER`: default user in the service container (your choice)
    - `HTC_API_PORT`: port number of the service container on which the flask app is served (your choice)
    - `MAX_REQ_RATE`: maximum number of execution requests allowed per IP address

* Any modifications in `api.py` will be reflected automatically.

* The following files can be modified in realtime:
    - `assets/config.json`
    - `assets/error.log`

* C and C++ source files can added/updated/removed from `assets/src` in realtime. Just execute `assets/compile.sh` after any change.

* Binary files can be added/updated/removed from `assets/binary` in realtime.

* `input.py` makes API calls. Change `apiUrl` and accordingly.

* Run `sudo docker-compose up`.

Go hunt it!
