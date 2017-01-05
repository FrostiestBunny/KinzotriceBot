#!/usr/bin/env python3

import json
import discord

class Desires:
    def __init__(self):
        with open('desires.json', mode='r', encoding='utf-8') as f:
            self.desires_data = json.load(f)
            self.desire_emoji = None

    def save(self, fil="desires.json"):
        with open(fil, mode='w', encoding='utf-8') as f:
            json.dump(self.desires_data, f)

    def user_exists(self, id):
        return str(id) in self.desires_data

    def get(self, id, name=None):
        return self.desires_data[str(id)]['desires']

    def add_user(self, id, name):
        self.desires_data[str(id)] = {'name': name, 'desires': 5}
        self.save()

    def get_name(self, id):
        return self.desires_data[str(id)]['name']

    def add(self, id, num):
        self.desires_data[str(id)]['desires'] += num
        self.save()

    def sub(self, id, num):
        self.desires_data[str(id)]['desires'] -= num
        self.save()

    def set_emoji(self, emoji):
        self.desire_emoji = emoji

    def get_emoji(self):
        return self.desire_emoji

desires = Desires()
