# Interactive Autonomous Cognitive Entity User Interface (iACEui)

Thank you for taking a look at our demo. If you have any feedback or questions, please create a discussion in the repo tagging @samgriek and @inkpaper.

The goal of this demo is to provide a user frieldly interface to engineer prompts for the ACE Framework. As such, we included an MVP of the ACE Framework infra for testing and demonstration purposes.

<div style="background-color: #fff9e6; color: #333; border: 2px solid #ffcc00; border-radius: 5px; padding: 10px; font-weight: bold;">
  <span style="font-size: 24px; margin-right: 10px;">⚠️</span>To run The ACE Framework infra in this demo all prompts must be engineered and saved via the prompt engineering and testing UI.
</div>

## Contributors

@inkpaper
@samgriek

## Runing the backend

<div style="background-color: #e6f0ff; color: #333; border: 2px solid #3399ff; border-radius: 5px; padding: 10px; font-weight: bold;">
  <span style="font-size: 24px; margin-right: 10px;">📘</span>This guide assume you have opened iACEui folder as a project in VSCode. Take this into consideration and adapt to your personal setup.
</div>

### Step 1: Set up your environment

Create the .env file

```bash
cp src/ace/app/example.env src/ace/app/.env
```

Set your Open API key in the .evn file on this line:

```bash
OPENAI_API_KEY=<OPENAI API key>
```

Copy the .env file to all the layers

```bash
cp src/ace/app/.env src/ace/app/api/app
cp src/ace/app/.env src/ace/app/layer_1_aspirational
cp src/ace/app/.env src/ace/app/layer_2_global_strategy
cp src/ace/app/.env src/ace/app/layer_3_agent_model
cp src/ace/app/.env src/ace/app/layer_4_executive
cp src/ace/app/.env src/ace/app/layer_5_cognitive_control
cp src/ace/app/.env src/ace/app/layer_6_task_prosecution
```

### Step 2: Build the base image with

```bash
./build_base_image.sh
```

### Step 3: Start the api and database

Start only the api and database if you haven't yet engineered your agent's prompts through the UI

```bash
docker-compose up db api --build
```

### Step 4: Start and load the UI

Install dependencies

```bash
cd frontend && npm install
```

Run the server

```bash
npm run dev
```

### Step 5: Engineer your prompts

Experimentation is key here. The UI provides a way to engineer prompts and test theories before starting up the agent. Once everything is working as you expect and the prompts are saved, you can start the rest of the agent.

<div style="background-color: #e6f0ff; color: #333; border: 2px solid #3399ff; border-radius: 5px; padding: 10px; font-weight: bold;">
  <span style="font-size: 24px; margin-right: 10px;">📘</span>Built into the layers is the ability to prevent a message from being sent to the next layer.  This function detects if the layer wants to send a message with `none` which prvents the message from being sent
</div>

Existing strategy for detecting none

```python
def determine_none(input_text):
    match = re.search(r"\[Message\]\n(none)", input_text)

    if match:
        return "none"

    return input_text
```

You can adapt this function to work for your prompt engineering style. For example, a more robust option could be to engineer your prompts to require JSON like below, and align the `determine_none` function.

```json
{
    "bus": "data",
    "message": "nothing much to say right now",
    "send": false,
}
```

<div style="background-color: #e6ffe6; color: #333; border: 2px solid #66ff66; border-radius: 5px; padding: 10px;">
  <span style="font-size: 24px; margin-right: 10px;">💡 Tips for egineering prompts</span>
  <ul style="font-weight: bold;">
    <li>Use the ACE Framework markdown file as a guide: <a href="https://github.com/daveshap/ACE_Framework/blob/main/ACE_Framework.md">ACE_Framework.md</a></li>
    <li>Come up with a strategy for the format of the messages on the bus. JSON is a solid choice but markdown can work well also</li>
    <li>Start with the Ancestral Prompt.  This prompt provides the overall context of the ACE Framework which is used at every level</li>
    <li>Prompt and test one layer at a time starting with the Aspirational Layer.</li>
    <li>Test that your reasoning and input messages yield the desired bus messages to the adjacent layers</li>
    <li>Come up with a way for the layer to not send a message when it isn't necessary as unnecessary chatter is problematic</li>
  </ul>
</div>

### Step 6: Run the ACE Framework

Given that the prompt engineering is complete, you can run the ACE Framework with the following command:

```bash
docker-compose up --build
```

the `--build` option is only required if you made code changes

<div style="background-color: #e6f0ff; color: #333; border: 2px solid #3399ff; border-radius: 5px; padding: 10px; font-weight: bold;">
  <span style="font-size: 24px; margin-right: 10px;">📘</span>Cognitive circuits, integrations, and more advanced funcitonality is not part of this demo, and I encourage you to Fork the repository and open a pull request to contribute!
</div>

## Check out the API docs

open the swagger docs:

```bash
http://0.0.0.0:8000/docs
```
