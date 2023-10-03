# iACEui

## Interactive Autonomous Cognitive Entity User Interface

### Runing the backend

#### First build the base image with:
```bash
./build_base_image.sh
```

#### Then start the backend with:
```bash
docker-compose up --build
```
the `--build` option is only required if you made code changes to the backend

#### To provide the ACE Agent a mission open the api docs and submite a request:

open the swagger docs:
```
http://0.0.0.0:8000/doc
```

send a request to this endpoint:
```
/send-mission/
```