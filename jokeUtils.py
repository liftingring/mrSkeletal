import discord
import asyncio
import random
import pickle 
import os
import json
import time
import csv
import botUtils

  
# Opening JSON file 
filename="DB.json"

f = open(filename, encoding="utf8") 
  
# returns JSON object as  
# a dictionary 
data = json.load(f) 
print(data[0])