import multiprocessing
import flask_app
import discord_bot

if __name__ == '__main__':
    flask_process = multiprocessing.Process(target=flask_app.run)
    discord_process = multiprocessing.Process(target=discord_bot.run)

    flask_process.start()
    discord_process.start()

    flask_process.join()
    discord_process.join()
