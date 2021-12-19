from client import send, setup
import random
import time

setup()

scores = {}

for x in range(0,10):  
   scores = send(f"{x} {random.randint(0,100)}") 
   time.sleep(0.5) 

print(scores)



for x in range(0,10):  
   scores = send(f"{x} {random.randint(0,100)}") 
   time.sleep(0.5) 

print(scores)

send("!DISCONNECT")

