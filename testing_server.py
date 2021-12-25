import random
import time
from client import setup, send_message

setup()

scores = {}

for x in range(0,10):  
   scores = send_message(f"{x} {random.randint(0,100)}") 
   time.sleep(0.5) 

print(scores)



for x in range(0,10):  
   scores = send_message(f"{x} {random.randint(0,100)}") 
   time.sleep(0.5) 

print(scores)

send("!DISCONNECT")

