# iACEui

## Interactive Autonomous Cognitive Entity User Interface

### Runing the backend

#### Step 1: Set up your environment
```bash
mv src/ace/app/api/example.env src/ace/app/api/.env
```
Set you Open API key in the .evn file on this line:
```bash
OPENAI_API_KEY="<your api key>"
```

#### Step 2: Build the base image with:
```bash
./build_base_image.sh
```

#### Step 3: Start the backend with:
- Start the full stack
```bash
docker-compose up --build
```
the `--build` option is only required if you made code changes to the backend

- In some cases you may want to just start the API
```bash
docker-compose up db api --build
```
### Check out the API docs for usage details

open the swagger docs:
```bash
http://0.0.0.0:8000/docs
```
