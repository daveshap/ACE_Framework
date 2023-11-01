# Interactive Autonomous Cognitive Entity User Interface (iACEui)

Thank you for exploring our demo. If you have feedback or questions, feel free to create a discussion in the repo and tag @samgriek and @inkpaper.

This demo aims to provide a user-friendly interface to engineer prompts for the ACE Framework, including an MVP of the ACE Framework infra for testing and demonstration.

> ⚠️ **Important:** To run the ACE Framework infra in this demo, prompts for all layers must be engineered and saved via the prompt engineering and testing UI.

## Contributors

@inkpaper
@samgriek

## Running the Backend

> 📘 **Note:** This guide assumes you have opened the iACEui folder as a project in VSCode. Please adapt these instructions to suit your personal setup.

### Step 1: Set up your environment

Create the .env file:

```bash
cp src/ace/app/example.env src/ace/app/.env
```

Set your OpenAI API key in the .env file:

```bash
OPENAI_API_KEY=<Your OpenAI API key>
```

Copy the .env file to all the layers:

```bash
cp src/ace/app/.env src/ace/app/api/app
cp src/ace/app/.env src/ace/app/layer_1_aspirational
cp src/ace/app/.env src/ace/app/layer_2_global_strategy
cp src/ace/app/.env src/ace/app/layer_3_agent_model
cp src/ace/app/.env src/ace/app/layer_4_executive
cp src/ace/app/.env src/ace/app/layer_5_cognitive_control
cp src/ace/app/.env src/ace/app/layer_6_task_prosecution
```

### Step 2: Build the base image

```bash
./build_base_image.sh
```

### Step 3: Start the API and Database

Start only the API and database if you haven't yet engineered your agent's prompts through the UI:

```bash
docker-compose up db api --build
```

### Step 4: Start the Svelte UI

Install dependencies:

```bash
cd frontend && npm install
```

Run the server:

```bash
npm run dev
```

### Step 5: Engineer your Prompts

Experiment and test your prompts through the UI before starting up the agent. Ensure all prompts are working as expected and are saved before proceeding.

> 📘 **Tip:** Built into the layers is the ability to prevent a message from being sent to the next layer. This function detects if the layer wants to send a message with `none`, preventing the message from being sent.

Existing strategy for detecting none:

```python
def determine_none(input_text):
    match = re.search(r"\[Message\]\n(none)", input_text)
    return "none" if match else input_text
```

You can adapt this function to suit your prompt engineering style.

> 💡 **Tips for Engineering Prompts:**

> - Use the ACE Framework markdown file as a guide: [ACE_Framework.md](https://github.com/daveshap/ACE_Framework/blob/main/ACE_Framework.md)
> - Decide on a format for the bus messages. Both JSON and Markdown are viable options.
> - Start with the Ancestral Prompt for overall context.
> - Prompt and test each layer starting with the Aspirational Layer.
> - Ensure your reasoning and input messages yield the desired bus messages for adjacent layers.
> - Implement a way for the layer to not send a message when it isn't necessary to avoid unnecessary system chatter.

### Step 6: Run the ACE Framework

With prompts engineered and saved, run the ACE Framework:

```bash
docker-compose up --build
```

Use the --build option if you've made code changes.

> 📘 **Note:** This demo does not cover cognitive circuits, integrations, or more advanced functionalities. We encourage you to fork the repository, make your own contributions, and submit a pull request!

## API Documentation

Access the Swagger API documentation at:
[Swagger Docs](http://0.0.0.0:8000/docs)

## Community Feedback and Insights

We've had some community members delve into the iACEui project, providing valuable insights on how it's set up, its key components, and its operation:

### Key Components

There are three main services driving the ACE Framework and the Frontend:

**Svelte GUI**: Interactive prompt engineering and testing user interface

**Postgres DB**: Stores identity, reasoning, and ancestral prompts, as well as system messages, control bus, and data bus prompts.

**RabbitMQ**: Serves as the pipeline for control and data busses, handling four messaging queues per layer for proper message passage.

**API**: Offers a variety of endpoints for starting, testing, and managing prompts in the system.  The `/mission` endpoint is used to provide the "user mission" to ACE.

## Additional Usage Tips

### On initial setup

- The Svelte frontend is served, allowing users to set prompts through the API and populate the Postgres DB.
- Once the DB is populated, the system is ready for launch.

### Operational Flow

- The system starts with a mission statement published to the aspirational layer via the `/mission` endpoint.
- The aspirational layer generates reasoning and separate control and data messages, which are then published and picked up by subsequent layers, continuing the cycle.  The subsequent layers in turn do the same.  Each layer subscribes and published to it's adjactent layers.  Control is passed down and Data is passed up the hierarchy.
