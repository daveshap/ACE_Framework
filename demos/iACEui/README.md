# iACEui

## Interactive Autonomous Cognitive Entity User Interface

### Runing the backend

#### Step 1: Set up your environment
- create the .env file
```bash
cp src/ace/app/example.env src/ace/app/.env
```
- Set you Open API key in the .evn file on this line:
```bash
OPENAI_API_KEY=<OPENAI API key>
```
- Copy the .env file to all the services
```bash
cp src/ace/app/.env src/ace/app/api/app
cp src/ace/app/.env src/ace/app/layer_1_aspirational
cp src/ace/app/.env src/ace/app/layer_2_global_strategy
cp src/ace/app/.env src/ace/app/layer_3_agent_model
cp src/ace/app/.env src/ace/app/layer_4_executive
cp src/ace/app/.env src/ace/app/layer_5_cognitive_control
cp src/ace/app/.env src/ace/app/layer_6_task_prosecution
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
