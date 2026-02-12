from app.services.llm_service import get_llm_service
import asyncio

async def main():
	

    from app.database import init_db
    init_db()

if __name__ == '__main__':
	
	asyncio.run(main())