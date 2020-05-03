import discord
import asyncio
import random
import pickle 
import os
import json
import time
import csv
import botUtils
import triviaUtils
import discordUtils

client=discord.Client()
token="NzA1MjQxODE5MDc5OTAxMjQ0.XqqvbA.HoiCIVO72Mm_OF1aTR9eewyF03s"
messages=[]
whoCounter=botUtils.whoCounter
triviaScores={}
activeQuestion=False
answers=[]
channel=0
winningScore=10
timer=40
activeGame=False




async def update_stats():
	await client.wait_until_ready()
	global messages,whoCounter

	while not client.is_closed():
		try:
			with open("stats.txt") as json_file:
				data=json.load(json_file)
				if data=={}:

					data['messages']=[]
				for msg in messages:
					data['messages'].append({
						'time': int(msg.time),
						'user': str(msg.user),
						'channel': str(msg.channel),
						'msg': str(msg.msg)
						})
			with open("stats.txt","w") as outfile:
				json.dump(data,outfile) 
			messages=[]
			await asyncio.sleep(300)

		except Exception as e:
			print(e)
			await asyncio.sleep(300)


async def trivia_Question():
	
	await client.wait_until_ready()
	global answers,triviaScores,activeQuestion,channel,timer,activeGame
	

	#while activeQuestion and not client.is_closed():
	while not client.is_closed():

		if activeQuestion:
			try:
				firstInterval=timer-10
				question=triviaUtils.getQuestion()
				await channel.send(question.parsed)
				await asyncio.sleep(firstInterval)
				await channel.send("You have 10 more seconds.")
				await asyncio.sleep(10)
				triviaScores=triviaUtils.updateScores(triviaScores,question,answers)
				#print(answers)
				await channel.send(f'Good job! The correct answer is {question.correctChoice}, {question.correctAnswer}.')
				answers=[]
				await asyncio.sleep(3)
				await channel.send(f'Calculating your scores....doot doot....beep')
				await asyncio.sleep(2)
				#print(triviaScores)
				msg=triviaUtils.printScores(triviaScores,"pts")
				await channel.send(msg)
				if triviaUtils.isGameOver(triviaScores,winningScore):
					winner=triviaUtils.winner(triviaScores)
					msg=f'We have a winner, congratulations {winner}!'
					triviaUtils.updateLeaderboard(winner)
					await channel.send(msg)
					await asyncio.sleep(2)
					await channel.send(triviaUtils.printLeaderboard())
					triviaScores={}
					activeGame=False


				activeQuestion=False
			except Exception as e:
				print(e)
				await asyncio.sleep(10)
		else:
			await asyncio.sleep(5)

def setWinningScore(content):
	global winningScore
	try:
		newScore=int(content[8:])
		winningScore=newScore
		return 0
	except Exception as e:
		print(e)

		return 1

def setTimer(content):
	
	global timer
	try:
		newTimer=int(content[10:])
		if newTimer<=15:
			return -1
		timer=newTimer
		
		return 0
	except Exception as e:
		print(e)
		return 1
			

		
			
client.loop.create_task(trivia_Question())
client.loop.create_task(update_stats())





@client.event
async def on_ready():
	print('logged in as')
	print(client.user.name)
	print(client.user.id)
	print('----')

@client.event
async def on_message(message):
	global messages,whoCounter,activeQuestion,answers,channel,triviaScores,winningScore,timer,activeGame

	mods=["coronasan#3763"]

	bot=client.user
	author=message.author
	#print(type(author))
	authorString=str(author)
	msg=message.content
	content=msg.lower()
	channel=message.channel
	newMsg=discordUtils.discordMsg(time.time(),author,channel,content)
	guild=message.guild
	#print(client.guilds)
	#print(message.channel)
	#print(message.guild)
	

	#we always log messages, need that data slurp
	messages.append(newMsg)
	#don't respond to self!
	if author==bot:
		return
	#take an answer if question is active, it is an answer, and they haven't answered
	elif activeQuestion and triviaUtils.isAnAnswer(content) and not triviaUtils.hasAnswered(author,answers):
		answers=triviaUtils.updateAnswers(author,content,answers)
		return

	#ignore any messages while question is going on
	elif activeQuestion: 
		return

	#elif content.startswith("!gmrequest"):
	#	discordUtils.requestGM(author,guild)
	#	return

	#elif content.startswith("!gmqueue"):
	#	msg=discordUtils.printGMRequests()


	if authorString in mods:


		if content.startswith("!newgame"):
			await message.channel.send("Let's play!")
			triviaScores={}
			activeGame=True
			activeQuestion=True
			return

		elif  (content.startswith("!next")) and activeGame and not activeQuestion:
		#triggers subroutine 
			activeQuestion=True
			return

		elif (content.startswith("!wipe")) and not (activeQuestion):
			#wipes leaderboard
			triviaUtils.wipeLeaderboard()
			return
	

		elif content.startswith("!playto"):
			exitCode=setWinningScore(content)
			if exitCode:
				await message.channel.send("My bones don't understand.")
				return
			return

		elif content.startswith("!settimer"):
		
			exitCode=setTimer(content)
			if exitCode==1:
				msg="My bones don't understand."
			elif exitCode==-1:
				msg="My bones need more time."
			else:
				return


	if content.startswith("!help"):
		msg="Try !joke, !flip, !score, !playingTo, !leaderboard, !message. If you are a mod try !setTimer, !playTo, !newGame, !next, !wipe"
	elif content.startswith("!joke"):
		msg=botUtils.jokeMsg()

	elif content.startswith("!flip"):
		msg=botUtils.flipCoinMsg()

	elif content.startswith("!message"):
		msg=discordUtils.getMessage()

	elif content.startswith("!timer"):
		msg=f'Timer is {timer} seconds.'

	elif content.startswith("!leaderboard"):
		msg=triviaUtils.printLeaderboard()

	elif content.startswith("!supersecretgmcommand"):
		mods.append(authorString)

	elif content.startswith("!playingto"):
		msg=f'You are playing to {winningScore}. You can do it!'

	elif content.startswith("mirror mirror is the wall who is fairest who is all"):
			if authorString=="josika#0513":
				msg="IS YOU!"
			else:
				msg="NOT YOU, STINK!"

	elif content.startswith("!score"):

		msgTemp=triviaUtils.printScores(triviaScores,"pts")
		if msgTemp=="":
			msg="You didn't start the bones!"
		else:
			msg=msgTemp

	

	elif content.startswith("who"):

		whoCounter=botUtils.updateCounter(author,whoCounter)
		count=whoCounter[authorString]

		if authorString=="Paperbags#4075":
			msg="Boy Stink!"



		elif count==1:
			msg="I am Mr. Skeletal doot doot"
			
		else:
			if count==2:
				msg=f'I already told you once, {authorString}, my name is Mr. Skeletal. I wont tell you again.'
			elif count<5:
				msg=f'I told you {count-1} times {authorString}, my name is Mr. Skeletal. Please dont make me tell you again.'
			elif count<10: 
				msg=f'I command you to the inner sanctum of hell you dogfaced pony soldier! Begone!'
			else:
				msg='REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'
	else:
		return
	await message.channel.send(msg)
	return


client.run(token)