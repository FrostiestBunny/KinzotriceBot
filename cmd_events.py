#!/usr/bin/env python3

from UOBot import bot
import discord
from events import event_handler

@bot.group(pass_context=True)
async def events(ctx):
    """The prefix for events commands.
    """
    if ctx.invoked_subcommand is None:
        await bot.say('No such command.')

@events.command(name="add", pass_context=True)
async def add_event(ctx, ev_name):
    """Adds an event.
    """
    author = ctx.message.author
    ev_metadata = {}
    if not event_handler.event_exists(ev_name):
        await bot.say('Official name of the event: ')
        msg = await bot.wait_for_message(author=author)
        ev_metadata['name'] = msg.content
        await bot.say('Description of the event: ')
        msg = await bot.wait_for_message(author=author)
        ev_metadata['desc'] = msg.content
        await bot.say('Date of the event (dd-mm-yyyy): ')
        msg = await bot.wait_for_message(author=author)
        ev_metadata['date'] = msg.content
        await bot.say('Participants (just type everybody for EVERYBODY, otherwise do participant1, participant2, etc. Use their original usernames.): ')
        msg = await bot.wait_for_message(author=author)
        ev_metadata['participants'] = msg.content
        await bot.say('Creator of the event(me if creator == message author): ')
        msg = await bot.wait_for_message(author=author)
        if msg.content == "me":
            msg.content = author.name
        ev_metadata['creator'] = msg.content

        ev_metadata['added_by'] = author.name
        event_handler.add(ev_name, ev_metadata)
    else:
        await bot.say('Event already registered.')
        return

    await bot.say('Event successfully added.')

@events.command(name="check")
async def check_event(ev_name : str):
    '''Checks if given event exists.
    '''
    if event_handler.event_exists(ev_name):
        ev_metadata = event_handler.get_event(ev_name)
        await bot.say(ev_metadata)
    else:
        await bot.say('No such event.')

@events.command(name="delete", pass_context=True)
async def delete_event(ctx, ev_name : str):
    '''Deletes given event.
    '''
    if event_handler.event_exists(ev_name):
        author = ctx.message.author
        ev_metadata = event_handler.get_event(ev_name)
        if ev_metadata['added_by'] == author.name or ev_metadata['creator'] == author.name:
            event_handler.remove(ev_name)
            await bot.say('Event successfully deleted.')
        else:
            await bot.say("You wish but you're not the one who added it, nor the creator.")
    else:
        await bot.say('No such event.')
