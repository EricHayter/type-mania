import asyncio
import time

num = 0

async def periodic(number):
    while True:
        number += 1
        await asyncio.sleep(1)

def stop():
    task.cancel()

loop = asyncio.get_event_loop()
task = loop.create_task(periodic(num))

try:
    loop.run_until_complete(task)
except asyncio.CancelledError:
    pass

while 1:
    print("is this working?")
    print(num)