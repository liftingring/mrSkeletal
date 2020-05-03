import discord
import asyncio
import random
import pickle 
import os
import json
import time
import csv

requests={}

statsFile="stats.txt"

class discordMsg:
	def __init__(self,time,user,channel,msg):
		self.time=time
		self.user=user
		self.channel=channel
		self.msg=msg

def requestGM(user,guild):
	print(requests)
	if guild not in requests:
		requests[guild]=[]
	if user in requests[guild]:
		return
	else:
		requests[guild].append(str(user))

def printGMRequests():
	if requests=={}:
		return "No requests for bone king"
	msg="\n".join([f'{str(key)} {", ".join(requests[key])}' for key in requests])
	return msg



def getMessage():
	global statsFile
	with open(statsFile, encoding="utf8") as f:

		data = json.load(f)["messages"]
		msg=random.choice(data)
	
	return f'{time.ctime(msg["time"])}: {msg["user"]}: {msg["msg"]}'
	
	 



