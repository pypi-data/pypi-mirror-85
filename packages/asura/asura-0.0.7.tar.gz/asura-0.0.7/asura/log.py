from color import ASOR

async def info(text: str):
	print(f"{ASOR.DYELLOW}{text}")

async def error(err: str):
	print(f"{ASOR.DRED}{err}")
