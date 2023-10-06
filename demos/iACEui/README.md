# iACEui

## Interactive Autonomous Cognitive Entity User Interface

### Runing the backend

#### First build the base image with:
```bash
./build_base_image.sh
```

#### Then start the backend with:
- Starte the full stack
```bash
docker-compose up --build
```
the `--build` option is only required if you made code changes to the backend

- In some cases you may want to just start the API
```bash
docker-compose up db api --build

#### To provide the ACE Agent a mission open the api docs and submite a request:

open the swagger docs:
```bash
http://0.0.0.0:8000/docs
```

send a request to this endpoint:
```bash
/send-mission/
```
