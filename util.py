#!/usr/bin/env python3

import UOBot

def math_check(message : UOBot.discord.Message):
    for n in range(10):
        if str(n) in message.content:
            if "+" in message.content or "-" in message.content or "*" in message.content or "=" in message.content:
                return True
    return False

def set_rps(*args):
    result = []
    for a in args:
        a = a.lower()
        if 'rock' in a:
            a = 'Rock'
        elif 'paper' in a:
            a = 'Paper'
        else:
            a = 'Scissors'
        result.append(a)
    result = tuple(result)
    return result

def eval_rps(a, b):
    if a == 'Rock':
        if b == 'Paper':
            return 'p2'
        if b == 'Scissors':
            return 'p1'
        return 'tie'
    if a == 'Paper':
        if b == 'Rock':
            return 'p1'
        if b == 'Scissors':
            return 'p2'
        return 'tie'
    if a == 'Scissors':
        if b == 'Rock':
            return 'p2'
        if b == 'Paper':
            return 'p1'
        return 'tie'
    return 0

#TODO JSON NOT TXT WHAT ARE YOU DOING
def saveTags(url, tag, tp):
    if tp == "img":
        tags = open('tagsImg.txt', 'a')
    else:
        tags = open('tagsVid.txt', 'a')
    tags.write('{0};{1}\n'.format(tag, url))
    tags.close()

def readTags(tag, tp):
    if tp == "img":
        tags = open('tagsImg.txt', 'r')
    else:
        tags = open('tagsVid.txt', 'r')
    tagsLines = tags.readlines()
    for line in tagsLines:
        if line.startswith(tag):
            (t, u) = line.split(";")
            tags.close()
            return u
def tagExists(tag, tp):
    if tp == "img":
        tags = open('tagsImg.txt', 'r')
    else:
        tags = open('tagsVid.txt', 'r')
    tagsLines = tags.readlines()
    for line in tagsLines:
        if line.startswith(tag):
            tags.close()
            return True
    tags.close()
    return False
