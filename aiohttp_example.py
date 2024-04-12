import aiohttp
import asyncio
import re
import aiofiles
import time
import requests

def get_data():
    data = get_ref()
    output =[]
    with requests.Session() as s:
        for i in data:
            with open("s.get(i).content)
    return 

def get_ref():
    with open("x.html", 'r', encoding='utf-8',
        errors='ignore') as fdata:
        data = fdata.read()
    img = re.compile(r'(\"http.+\.)(png|jpg)(\")')
    images = re.findall(img,data)
    return ["".join(x)[1:-1] for x in images]
    
async def get_images(ref):
    async with aiohttp.ClientSession() as session:
        async with session.get(ref) as response:
            return (await response.read())



async def save_images(img):
    async with aiofiles.open(f"{hash(img)}.png",mode="wb") as f:
        await f.write(img)


async def main():
    a = get_ref()
    da =[]
    for r in a:
        da.append(await get_images(r.strip()))
    for i in da:
        await save_images(i)
start = time.time()
asyncio.run(main())
print(time.time()-start)
