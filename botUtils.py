import discord
import asyncio
import random
import pickle 
import os
import json
import time
import csv

whoCounter={}


def jokeMsg():
    with open("shortjokes.csv") as f:
        reader = csv.reader(f)
        chosen_row = random.choice(list(reader))
        return chosen_row[1]

def flipCoinMsg():
    flip=random.choice(['Heads','Tails'])
    msg=f'Flip a dip, {flip}! Oww my aching bones :('
    return msg

def updateCounter(author,counter):
   
    s=str(author)
    if s in counter:
        
        counter[s]+=1
    else:
        counter[s]=1
    return counter
