# Stacey
![stacey-160.png](frontend/public/images/stacey-160.png)

This a simple but fun demo prototype for the ACE framework.

## Capabilities
This is a prototype, so all the code is work-in-progress and simplistic.

But it is helping us evolve and explore the framework, and she can already do some pretty cool stuff.
- Chat with her through Discord or Web chat.
- She is self-aware (well, more like her prompt causes her to act as if she was self-aware), and knows that she is an evolving prototype of the ACE framework, which makes for some pretty interesting conversations. 
- See her internal state live using a web admin UI
- She can embed auto-generated images and gifs ("Draw me cat image", "Make a dancing banana gif"), or even multiple images ("Draw me a 3-frame cartoon about how we used AI to solve climate change")
- She can read web pages ("Summarize the contents of http://.....")
- She follow aspirations and guidance from the aspirational layer (although it is really just a prompt for now) 
- She dynamically decide when she should or shouldn't respond to messages, based on social cues
- She has a pretty colorful personality which can be customized
- She knows what time it is and where she is hosted
- She has long-term memory (via a vector db), can figure out which things are worth remembering, and will recall memories relevant to the context. She can also be asked to forget things.
- She is autonomous. She can set an internal alarm clock to wake up and do things in the future. For example "Stacey, ping me in this channel in 30 seconds". So she sleeps by default, but is woken up by incoming messages and by her own alarm clock. Every time she goes back to sleep, she figures out when it makes sense to wake up next.
- She maintains a "whiteboard", a dynamically updated state of the world. For example "I have agreed to be Henrik's health coach. For starters, I will remind him to stand up every hour (next time is 18:55)". She automatically updates it when needed and includes it with every prompt. 

## Reflection & caveats

- The current implementation of Stacey is actually surprisingly fun and useful. We've had her running on our internal discord during her whole development, bantering with her on a daily basis. She really only uses the Agent layer right now. The code includes an implemention of the Bus system, and stubs for the other layers, but this wasn't needed for Stacey's current capabilities. So there is some unused code in the system right now. 

- Our initial implementation was more complex, using both Buses, the aspirational layer, and the global strategy layer. But the added complexity actually made the agent less useful and prone to strange behaviors. For this particular use case, it turned out that simpler was better. 

- We ended up using just the Agent layer and offloaded most of the work to the LLM instead, leveraging its innate capabilities. If we work more on this prototype, then we might explore using more layers of the framework, and splitting some of her current cognitive capabilities into different layers of the framework.

## Using GPT as an Action Decider

One useful reusable idea was how we work with Actions. Normally when using an LLM you ask it to generate responses. Stacey, however, asks the LLM to generate actions, and sending a message to a user is just one of many possible actions.

This is an alternative to GPT function calling. GPT function calling is limited because it can only trigger one function at a time. With actions, we expect a list of actions from the LLM. For example:

```json
[
    {
        "action": "get_web_content",
        "url": "https://example.com"
    },
    {
        "action": "send_message",
        "content": "OK I'll ping you in 30 seconds, and give you a summary of that web page."
    },
    {
        "action": "set_next_alarm",
        "time_utc": "2023-01-30T13:45:00Z"
    },
    {
        "action": "update_whiteboard",
        "contents": "I should ping Henrik at 2023-01-30T13:45:00Z"
    }
]
```

- Actions are executed in parallell, which saves a lot of time and cost. Otherwise we would have to send the whole chat history back to the LLM for every action, pay for the tokens, and wait for a response.
- Actions that don't have a return value (such as update_whiteboard and send_message) are considered "fire and forget", so there is no need to send anything more to the LLM.
- Actions that do have a return value (such as get_web_content) will send the output back to the LLM for further processing (including chat history). Basically the way GPT function calling works. 

# Running Stacey

## Running the backend
- `cd backend`
- `cp .env.example .env` and set the keys
- `pip install -r requirements.txt`
- `python main.py`

That runs both the web server and the discord bot.

You can also run just one or the other:
- `python main_web.py`
- `python main_discord.py`

Surf to http://localhost:5000/chat?message=hi to test the backend & openai connection.

## Running the vector DB

Stacey uses a vector DB to store and retrieve her knowledge.
Currently it is hard-coded to Weaviate.

If you have [docker compose](https://docs.docker.com/compose/install/) you can simply run `config/examples/docker-compose.yml`.

- `cd config/examples`
- `docker-compose up`

Note that the sample docker-compose file has some commented out lines that you can use to configure where
the memories are stored on disk. If you don't do this, the memories will disappear if the docker container is removed.
Useful for testing, but for production you probably want to store the memories on disk.

## Running the frontend
- `cd frontend`
- `cp .env.example .env.local`
- `npm install`
- `npm run dev`

Surf to http://localhost:3000 and start interacting with the bot.

## Discord

Here's info about to get Stacey into a discord server
https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro