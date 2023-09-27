# Stacey
This a work-in-progress demo prototype for the ace framework.

Currently this is a simple GPT chatbot that you can talk to through the web or discord.

## Backend
- `cd backend`
- `cp .env.example .env` and set the keys
- `pip install -r requirements.txt`
- `python main.py`

That runs both the web server and the discord bot. You can also run just one or the other.
- `python app.py`
- `python discord_bot.py`

Surf to http://localhost:5000/chat?message=hi to test the backend & openai connection.

## Frontend
- `cd frontend`
- `npm install`
- `npm run dev`

Surf to http://localhost:3000