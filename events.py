#!/usr/bin/env python3

import json
import discord

class Events:
    def __init__(self):
        with open('events.json', mode='r', encoding='utf-8') as f:
            self.events_data = json.load(f)

    def save(self, fil='events.json'):
        with open(fil, mode='w', encoding='utf-8') as f:
            json.dump(self.events_data, f)

    def add(self, name, metadata):
        self.events_data[name] = metadata
        self.save()

    def event_exists(self, name):
        return name in self.events_data

    def get_event(self, name):
        return self.events_data[name]

    def remove(self, name):
        del self.events_data[name]
        self.save()

event_handler = Events()
