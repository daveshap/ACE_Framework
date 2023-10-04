import asyncio

from main import stacey_main

if __name__ == '__main__':
    asyncio.run(stacey_main(start_discord=False, start_web=True))