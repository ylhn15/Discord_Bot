import json
import discord
import asyncio
import random
import sys
import urllib.request
import googlesearch
from bs4 import BeautifulSoup

TOKEN = 'token'

client = discord.Client()

@client.event
async def on_message(message):
    # we do not want the bot to reply to itself
    json_data=open("quotes.json").read()
    quotes = json.loads(json_data)
    if message.author == client.user:
        return
    if message.content.startswith('!quote'):
        await message.channel.send(get_random_quote(message, quotes))
    if message.content.startswith('!lyrics'):
        await message.channel.send(get_lyrics(message))
    if message.content.startswith('!addQuote'):
        await message.channel.send(add_quote(message))

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

def get_random_quote(message, quotes):
    random_number = random.randint(0, (len(quotes)-1))
    quote = str(quotes[random_number])
    if "by" not in quote:
        quote = "\"" + str(quotes[random_number]) + "\" - Taylor Swift"
    else:
        quote = "\"" + quote.replace("by ", "\" - ")
    # msg = '{0.author.mention} {quote}'.format(message)
    return quote


def add_quote(message):
    newQuote = message.content.split(" ", 1)[1].replace("\"","")
    if "by" not in newQuote:
        return "Format: {Zitat} by {Autor}"
    quotes.append(newQuote)
    with open('quotes.json', 'w') as fp:
        json.dump(quotes, fp)
    return "added quote \"" + newQuote + "\" to quotes"


def get_lyrics(message):
    url =""
    for text in message.content.split(" ", 1):
        url += text
        url += " "
    url += "lyrics"
    print(url)
    num_page = 1
    search_results = googlesearch.search(url, stop=100)
    for result in search_results:
        if "songtexte.com" in result:
            print(result)
            if len(result) > 0:
                page = urllib.request.urlopen(result)
                soup = BeautifulSoup(page.read(), 'html.parser')
                print(soup.find(id="lyrics").get_text())
                return soup.find(id="lyrics").get_text()


client.run(TOKEN)
