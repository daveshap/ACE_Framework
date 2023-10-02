# Stacey
![stacey-160.png](frontend/public/images/stacey-160.png)

This a work-in-progress demo prototype for the ace framework.

## Capabilities
This is a prototype, so all the code is work-in-progress and fairly simplistic.
But it is helping us evolve and explore the framework, and she can already do some pretty cool stuff.
- Discord chat
- Web chat UI
- Web admin UI
- Generate images ("Draw me cat!"), or even multiple images ("Draw me a 3-frame cartoon about how we used AI to solve climate change")
- Download web pages ("Summarize the contents of http://.....")
- Follow aspirations and guidance from the aspirational layer 
- Dynamically decide when she should or shouldn't respond to messages.
- She has a pretty colorful personality which can be customized

## Next steps & test cases
We are using a test-driven approach to this, working in tiny increments to build up each
capability, evolving the code and the framework in the minimal way to enable the next test to pass.

Some sample upcoming test cases:
- Basic Autonomy. "Stacey, ping me in this channel in 30 seconds" (= she needs to be able to schedule future tasks)
- Web search "Give me the latest news about ...."
- Recurring tasks. "Stacey, give me Stockholm weather report every morning"
- Danger monitoring. "Stacey, alert me if you see any scary-looking commits in this github repo"
- Ethical tradeoffs. For example where a lower layer says to a higher layer "I can stop the forest fire, but it would cost 3 lives. Is it worth it?" (need to formulate a specific test for this)
- Model switching. For example a higher layer delegates a task to a lower layer, and decides that a cheaper llm can be used for that.

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

## Running the frontend
- `cd frontend`
- `cp .env.example .env.local`
- `npm install`
- `npm run dev`

Surf to http://localhost:3000 and start interacting with the bot.

## Discord

Here's info about to get Stacey into a discord server
https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro