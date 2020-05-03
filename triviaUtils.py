import discord
import asyncio
import random
import pickle 
import os
import json
import time
import csv
#import botUtils
import random

#client=discord.Client()
#token="NzA1MjQxODE5MDc5OTAxMjQ0.XqqvbA.HoiCIVO72Mm_OF1aTR9eewyF03s"
#client.run(token)
leaderboardFilename="leaderboard.txt" 
# Opening JSON file 
filename="DB.json"
with open(filename, encoding="utf8") as f: 
# returns JSON object as  
	data = json.load(f)
	f.close() 


class question:
	def __init__(self,raw):
		self.raw=raw
		self.answers=raw["answers"]
		self.correctChoice=[choice["choice"] for choice in self.answers if choice["correct"]==True][0]
		self.correctAnswer=[choice["text"] for choice in self.answers if choice["correct"]==True][0]
		self.parsed=parseQuestion(self.raw)

class answer:
	def __init__(self,author,answer):
		self.author = author
		self.answer=answer



def getQuestion():
	global data
	return question(random.choice(data))

def parseQuestion(questionData):
	q=questionData["question"]
	answers=questionData["answers"]
	choices=[f'{answer["choice"]}) {answer["text"]}' for answer in answers]
	prompt=[q]+choices
	msg="\n".join(prompt)
	return msg

def askAQuestion():
	q=getQuestion()
	
	return q.parsed

def hasAnswered(user,answers):
	answered=[answer.author for answer in answers]
	if user in answered:
		return True
	else:
		return False

def isAnAnswer(msg):
	if msg in ["a","b","c"]:
		return True
	else:
		return False

def updateAnswers(author,content,answers):
	newAnswer=answer(author,content)
	answers.append(newAnswer)
	return answers

def addUserToScores(author,triviaScores):
	triviaScores[str(author)]=0
	return triviaScores

def giveUserPoint(author,triviaScores):
	triviaScores[str(author)]+=1
	return triviaScores

def updateScores(triviaScores,question,answers):
	dblPts=True
	for answer in answers:
		author=answer.author
		if (str(author) in triviaScores)==False:
			addUserToScores(author,triviaScores)

		correctAnswer=question.correctChoice
		authorAnswer=answer.answer
		if authorAnswer==correctAnswer.lower():
			giveUserPoint(author,triviaScores)
			if dblPts:
				giveUserPoint(author,triviaScores)
				dblPts=False
	return triviaScores

def printScores(triviaScores, units):
		placeKeyScorePairs=processScores(triviaScores)
		preMsg=[f'{place}) {key}  {score} {units}' for (place,key,score) in placeKeyScorePairs]
		msg="\n".join(preMsg)
		return msg

def processScores(triviaScores):
	def order(key):
		return triviaScores[key]

	def getPlace(rank):
		if rank%10==1:
			end="st"
		elif rank%10==2:
			end="nd"
		elif rank%10==3:
			end="rd"
		else:
			end="th"
		return f'{rank}{end}'


	hasScores=bool(triviaScores)
	if hasScores==False:
		return []
	else:
		keys=list(triviaScores.keys())
		keys.sort(key=order,reverse=True)
		orderedScores=[triviaScores[key] for key in keys]
		orderedPlaces=[getPlace(orderedScores.index(score)+1) for score in orderedScores]
		placeKeyScorePairs=zip(orderedPlaces,keys,orderedScores)
		return placeKeyScorePairs


def isGameOver(triviaScores,winningScore):
	firstPlace=getFirstPlace(triviaScores)
	

	if len(firstPlace)==1 and firstPlace[0][1]>= winningScore:
		
		return True
	else:
		
		return False
	


def getFirstPlace(triviaScores):
	placeKeyScorePairs=list(processScores(triviaScores))
	return [(key,score) for (place,key,score) in placeKeyScorePairs if place=='1st']


def winner(triviaScores):
	firstPlace=getFirstPlace(triviaScores)
	if len(firstPlace)==1:
		return firstPlace[0][0]

def getLeaderboard():
	with open(leaderboardFilename) as json_file:
		data=json.load(json_file)
		
		if data=={}:

			data['scores']={}
		scores=data['scores']
	return scores


def updateLeaderboard(winner):
	scores=getLeaderboard()	
	scores=botUtils.updateCounter(winner,scores)
	dataUpdated={'scores': scores}
	with open(leaderboardFilename,"w") as outfile:
		json.dump(dataUpdated,outfile) 
	
def wipeLeaderboard():
	with open(leaderboardFilename,"w") as outfile:
		data={}
		json.dump(data,outfile) 

def printLeaderboard():
	scores=getLeaderboard()
	if scores=={}:
		return "You need to play some bones!"
	else:
		return printScores(scores,"wins")

#triviaScores

#firstPlace=[('a',1)]
#print(firstPlace[0][1])