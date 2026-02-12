from app.services.llm_service import get_llm_service
import asyncio

async def main():
	llm = get_llm_service()
	content, provider = await llm.generate("Commnent être abondant ?")
	print(provider, content)


if __name__ == '__main__':
	asyncio.run(main())