#!/usr/bin/env python3

from desires import desires
import discord
from UOBot import bot
import random

@bot.command(name="OH_DESIRE", pass_context=True)
async def check_desires(ctx, member : discord.Member=None):
    '''Shows your current desires balance.
    '''
    if not member:
        member = ctx.message.author
    if not desires.user_exists(member.id):
        desires.add_user(member.id, member.name)
    await bot.say('{} has {} {}.'.format(member.name, desires.get(member.id), desires.get_emoji()))

@bot.command(name="lottery", pass_context=True)
async def desires_lottery(ctx):
    '''Chooses a random person to award 1 desire to.
    '''
    to_choose = []
    server = ctx.message.server
    for member in server.members:
        if member.bot:
            continue
        to_choose.append(member)
    chosen = random.choice(to_choose)
    await bot.say('{} has won the lottery. Awarding 1 {}.'.format(chosen.name, desires.get_emoji()))
    desires.add(chosen.id, 1)

@bot.command(name="award", pass_context=True)
async def award_desires(ctx, number : int, *members : discord.Member):
    '''Awards desires to given user. BOT OWNER ONLY.
    '''
    if ctx.message.author.id != "178887072864665600":
        await bot.say('You wish.')
        return
    members = list(members)
    msg = ""
    for member in members:
        try:
            desires.add(member.id, number)
            msg += member.name
            msg += ", "
        except KeyError:
            print("{} has no entry in the database.".format(member.name))
            continue
    await bot.say('Awarded {} {} to {}.'.format(number, desires.get_emoji(), msg))

@bot.command(name="coin_bet", pass_context=True)
async def coin_bet(ctx, guess : str, number : int):
    "Type heads or tails and then how much you bet."
    user = ctx.message.author
    number = abs(number)
    if number == 0 or desires.get(user.id) < number:
            await bot.say('Nope.')
            return
    coin = ["heads", "tails"]
    coin_guessed = random.choice(coin)
    if guess == coin_guessed:
        await bot.say('You win {} {}!'.format(number, desires.get_emoji()))
        desires.add(user.id, number)
    else:
        await bot.say('YOU LOSE, HAHA.')
        desires.sub(user.id, number)

@bot.command(name="give_desire", pass_context=True)
async def give_desire(ctx, user : discord.User, number : int):
    '''Transfers desires to given user.
    '''
    if user is None:
        await bot.say("No such user.")
        return
    giver = ctx.message.author
    number = abs(number)
    if desires.get(giver.id) < number:
        await bot.say('You wish.')
        return
    desires.sub(giver.id, number)
    desires.add(user.id, number)
    await bot.say('Desires sent.')

@bot.command(name="lb", pass_context=True)
async def desire_leaderboard(ctx):
    '''Gets the leaderboard with top ten users.
    '''
    await bot.send_typing(ctx.message.channel)
    lb_sorted = sorted(desires.desires_data, key=lambda des: desires.desires_data[des]['desires'])
    lb_sorted = reversed(lb_sorted)
    top_ten = ""
    counter = 0
    for k in lb_sorted:
        if desires.get_name(k) == 'Kinzotrice' or desires.get_name(k) == 'Nadeko' or desires.get_name(k) == 'Mirai':#Much faster than getting a user by id and then checking if they're a bot.
            continue
        if counter == 10:
            break
        counter += 1
        top_ten += desires.get_name(k)
        top_ten += ": "
        top_ten += str(desires.get(k))
        top_ten += "\n"
    await bot.say(top_ten)
