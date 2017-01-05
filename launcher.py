#!/usr/bin/env python3

from UOBot import bot
import games
import cmd_desires
import cmd_events
import os

bot.run(os.environ['KINZOTOKEN'])
