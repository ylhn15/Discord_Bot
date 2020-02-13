import json
import discord
import asyncio
import random
import sys
import urllib.request
import googlesearch
from textwrap import wrap
from bs4 import BeautifulSoup

TOKEN = 'TOKEN'

class MyClient(discord.Client):
    async def on_message(self, message):
        # we do not want the bot to reply to itself
        # json_data=open("quotes.json").read()
        # quotes = json.loads(json_data)
        if message.author == client.user:
            return
        if message.content.startswith('!quote'):
            await message.channel.send(get_random_quote(message, quotes))
        if message.content.startswith('!lyrics'):
            lyrics = self.get_lyrics(message)
            x = 1999
            chunks = ([lyrics[i: i + x] for i in range(0, len(lyrics), x)])
            for text in chunks:
                await message.channel.send(text)
        if message.content.startswith('!addQuote'):
            await message.channel.send(add_quote(message))

    async def on_ready(self):
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    def get_random_quote(self, message, quotes):
        random_number = random.randint(0, (len(quotes)-1))
        quote = str(quotes[random_number])
        if "by" not in quote:
            quote = "\"" + str(quotes[random_number]) + "\" - Taylor Swift"
        else:
            quote = "\"" + quote.replace("by ", "\" - ")
            # msg = '{0.author.mention} {quote}'.format(message)
            return quote


    def add_quote(self, message):
        newQuote = message.content.split(" ", 1)[1].replace("\"","")
        if "by" not in newQuote:
            return "Format: {Zitat} by {Autor}"
        quotes.append(newQuote)
        with open('quotes.json', 'w') as fp:
            json.dump(quotes, fp)
            return "added quote \"" + newQuote + "\" to quotes"


    def get_lyrics(self, message):
        url =""
        for text in message.content.split(" ", 1):
            url += text
            url += " "
            url += "lyrics"
        search_results = googlesearch.search(url, stop=100)
        for result in search_results:
            if "songtexte.com" in result:
                print(result)
                if len(result) > 0:
                    page = urllib.request.urlopen(result)
                    soup = BeautifulSoup(page.read(), 'html.parser')
                    lyrics = soup.find(id="lyrics").get_text() 
                    # if len(lyrics) > 2000:
                    # print(soup.find(id="lyrics").get_text())
                    return lyrics

client = MyClient()
client.run(TOKEN)
