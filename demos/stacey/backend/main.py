import multiprocessing
import app
import discord_bot

if __name__ == '__main__':
    app_process = multiprocessing.Process(target=app.run)
    discord_process = multiprocessing.Process(target=discord_bot.run)

    app_process.start()
    discord_process.start()

    app_process.join()
    discord_process.join()
