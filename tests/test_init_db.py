import sys, os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import asyncio

async def main():
    from app.database import init_db
    init_db()

if __name__ == '__main__':
	asyncio.run(main())