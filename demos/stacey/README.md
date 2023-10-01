# Stacey
![stacey-160.png](frontend/public/images/stacey-160.png)

This a work-in-progress demo prototype for the ace framework.

Currently this is a simple GPT chatbot that you can talk to through the web or discord.
It also has a simple admin UI for seeing the framework in action.

## Backend
- `cd backend`
- `cp .env.example .env` and set the keys
- `pip install -r requirements.txt`
- `python main.py`

That runs both the web server and the discord bot.

You can also run just one or the other:
- `python main_web.py`
- `python main_discord.py`

Surf to http://localhost:5000/chat?message=hi to test the backend & openai connection.

## Frontend
- `cd frontend`
- `cp .env.example .env.local`
- `npm install`
- `npm run dev`

Surf to http://localhost:3000 and start interacting with the bot.

## Discord

Here's info about to get Stacey into a discord server
https://discordpy.readthedocs.io/en/stable/discord.html#discord-intro