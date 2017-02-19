#!/usr/bin/env python3

import discord
from discord.ext import commands
import random
import datetime
import requests
import util
import json
from desires import desires
import os
import re
import pickle

description = '''Removed kebab.'''
bot = commands.Bot(command_prefix='?', description=description)
imgSuf = ("png", "jpg", "jpeg", "gif", "gifv")
vidSuf = ("https://www.youtube", "http://www.youtube")
default_markov_input = {}
bee_movie = ""

@bot.event
async def on_ready():
    global bee_movie
    uo = None
    await bot.change_presence(game=discord.Game(name='achieving world domination'))
    servers = list(bot.servers)
    for server in servers:
        if server.name == "Umineko Online":
            uo = server
            break
    for emoji in uo.emojis:
        if emoji.name == "oh_desire":
            desires.set_emoji(emoji)
            break

    with open("logs.pickle", mode="rb") as f:
        pickle_data = pickle.load(f)

    pattern = re.compile(r"(\[\d{4}-\d{2}-\d{2}\])?\s*(.*?)\(.*?\):\s*(.*)", re.I)
    for line in pickle_data:
        match = re.match(pattern, line)
        if match:
            if match.group(2) not in default_markov_input:
                default_markov_input[match.group(2)] = [match.group(3)]
            else:
                default_markov_input[match.group(2)].append(match.group(3))

    with open("bee.txt", mode="r", encoding="utf-8") as f:
        bee_movie = f.read().replace('\n', '')
    for k in default_markov_input:
        default_markov_input[k] = " ".join(default_markov_input[k])
    print('Logged in as')
    print(bot.user.name)
    print('------')


@bot.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await bot.say(left + right)

@bot.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await bot.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await bot.say("You roled: {}".format(result))

@bot.command()
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await bot.say(random.choice(choices))

@bot.command(pass_context=True)
async def repeat(ctx, times : int, *args : str):
    """Repeats a message multiple times."""
    if times > 5:
        await bot.say("You wish.")
        return
    args = list(args)
    if "@everyone" in args or "@here" in args:
        content = "{}, you wish.".format(ctx.message.author.mention)
    else:
        content = " ".join(args)
    for i in range(times):
        await bot.say(content)

@bot.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await bot.say('{0.name} joined in {0.joined_at}'.format(member))

@bot.group(pass_context=True)
async def tag(ctx):
    """The prefix for tag commands.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No, {0.subcommand_passed} is not cool'.format(ctx))

#TODO: Change the tags to be stored in a json not some txt, ugh.
@tag.command(name='save', pass_context=True)
async def tag_save(ctx, tp : str, url : str, tag : str):
    """Saves a tag for further use. Usage: ?tag save [type] [url] [tag]
Available types so far: img, vid"""
    if ";" in tag:
        await bot.say("Can't use ';' in tag name.")
        return
    if util.tagExists(tag, tp):
        await bot.say('Tag already exists.')
        return
    if tp == "img":
        if str(url).endswith(imgSuf) == False:
            await bot.say('Not an image.')
            return
    else:
        if str(url).startswith(vidSuf) == False:
            await bot.say('Not a video.')
            return
    util.saveTags(url, tag, tp)
    await bot.say('Tag succefully saved.')

@bot.command(name='status')
async def status_change(*args):
    """Changes the 'game' the bot is playing."""
    status = " ".join(args)
    await bot.change_presence(game=discord.Game(name=status))

@bot.command(name='t', pass_context=True)
async def tag_show(ctx, tp : str, tag : str):
    """Displays the given tag. Usage: ?t type tag"""
    tagRead = util.readTags(tag, tp)
    try:
        await bot.say(tagRead)
    except discord.errors.HTTPException:
        await bot.say("No such tag.")

@bot.command()
async def nuke(*args):
    """Nukes given person."""
    ppl = " ".join(args)
    await bot.say("Nukes sent to {0}.".format(ppl))

#TODO: JSON NOT TXT
@tag.command(name="list")
async def list_tags(tp : str):
    """Lists all tags of the given type."""
    if tp == "img":
        tags = open('tagsImg.txt', 'r')
    else:
        tags = open('tagsVid.txt', 'r')
    tagList = []
    tagsLines = tags.readlines()
    for line in tagsLines:
        (t, u) = line.split(";")
        tagList.append(t)
    await bot.say(", ".join(tagList))

@bot.command(pass_context=True)
async def my_id(ctx):
    '''PMs you your unique user ID.
    '''
    aut = ctx.message.author
    await bot.send_message(aut, 'Your user ID is: {}'.format(aut.id))

@bot.command(name="avatar")
async def get_avatar(member: discord.Member):
    '''Displays your avatar.
    '''
    await bot.say(member.avatar_url)

@bot.command(name="weather")
async def get_weather(*args : str):
    '''Looks up current weather.
    '''
    location = " ".join(args)
    auto_complete = requests.get('http://autocomplete.wunderground.com/aq?query={}'.format(location))
    ac = json.loads(auto_complete.text)
    try:
        query = ac['RESULTS'][0]['l']
    except IndexError:
        await bot.say("Couldn't find the location because my algorithm sucks as of now.")
        return
    r = requests.get('http://api.wunderground.com/api/{}/conditions{}.json'.format(os.environ['WEATHERAPI'], query))
    to_decode = r.text
    js = json.loads(to_decode)
    w = js['current_observation']
    msg = "Current weather for: {} \n{} {}\n{}\nHumidity: {}\nWind: {}kph\nWind gust: {}kph\nFeels like: {}".format(w['display_location']['full'],
                                                   w['weather'],
                                                   w['icon_url'],
                                                   w['temperature_string'],
                                                   w['relative_humidity'],
                                                   w['wind_kph'],
                                                   w['wind_gust_kph'],
                                                   w['feelslike_string'])
    await bot.say(msg)

@bot.command()
async def purge_math(channel : discord.Channel):
    await bot.purge_from(channel, limit=20, check=util.math_check)

@bot.command(name="red")
async def convert_red(*args : str):
    msg = " ".join(list(args))
    await bot.say("```diff\n-{}\n```".format(msg))

@bot.command(pass_context=True)
async def dismiss(ctx):
    if ctx.message.author.id == '178887072864665600':
        await bot.say("Going to sleep.")
        await bot.logout()
    else:
        await bot.say("You wish.")
        return

@bot.command()
async def purge_fata(channel : discord.Channel):
    await bot.purge_from(channel, limit=50, check=util.fata_check)

@bot.command()
async def markov(member : str, order : int=4, gen_len : int=100):
    if order > 6:
        await bot.say("6 is max because what if you see some secret ERP?")
        return
    if gen_len > 500:
        await bot.say("The length is too big.")
        return
    data = default_markov_input
    if not member in data:
        await bot.say("No such member in the input data.")
        return
    ngrams = {}
    to_markov = data[member]

    for i in range(len(to_markov)-order):
        gram = to_markov[i:i+order]

        if not gram in ngrams:
            ngrams[gram] = []
        ngrams[gram].append(to_markov[i+order])


    current_gram = random.choice(list(ngrams.keys()))
    result = current_gram

    for i in range(gen_len):
        try:
            possibilities = ngrams[current_gram]
        except KeyError:
            await bot.say("There was some error. Sucks, don't it.")
            break
        if possibilities is None:
            break
        next = random.choice(possibilities)
        result += next
        length = len(result)
        current_gram = result[length-order:length]
    result = result.replace("\n", " ")
    await bot.say(result)

@bot.command()
async def markov_list():
    results = []
    counter = 0
    index = -1
    print(len(default_markov_input))
    for k in default_markov_input:
        if "[" in k or "]" in k:
            continue
        if counter % 100 == 0:
            results.append("")
            index += 1
        results[index] += k + " "
        counter += 1

    for r in results:
        await bot.say(r)

@bot.command()
async def beerkov(order : int=6, gen_len : int=100):
    if order > 6:
        await bot.say("No.")
        return
    ngrams = {}
    for i in range(len(bee_movie)-order):
        gram = bee_movie[i:i+order]

        if not gram in ngrams:
            ngrams[gram] = []
        ngrams[gram].append(bee_movie[i+order])

    current_gram = random.choice(list(ngrams.keys()))
    result = current_gram

    for i in range(gen_len):
        try:
            possibilities = ngrams[current_gram]
        except KeyError:
            await bot.say("There was some error. Sucks, don't it.")
            break
        if possibilities is None:
            break
        next = random.choice(possibilities)
        result += next
        length = len(result)
        current_gram = result[length-order:length]
    await bot.say(result)
