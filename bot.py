import json
import discord
import random
import urllib.request
import googlesearch
from bs4 import BeautifulSoup

with open('config.json') as json_file:
    try:
        data = json.load(json_file)
    except ValueError:
        print("config.json does not contain correct json")
        exit()

if data['token'] is None:
    print("Token not found in config.json. Please check your config.json file.")
    exit()
else:
    TOKEN = data['token']


class Bot(discord.Client):
    async def on_message(self, message):
        if message.author == client.user:
            return
        if message.content.startswith('!quote'):
            await message.channel.send(self.get_random_quote(message, quotes))
        if message.content.startswith('!lyrics'):
            lyrics = self.get_lyrics(message)
            if lyrics is None:
                await message.channel.send("Fehler: Songtext konnte nicht gefunden werden")
            max_chunk_size = 1999
            chunks = ([lyrics[i: i + max_chunk_size] for i in range(0, len(lyrics), max_chunk_size)])
            for text in chunks:
                await message.channel.send(text)
        if message.content.startswith('!addQuote'):
            await message.channel.send(self.add_quote(message))

    async def on_ready(self):
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    def get_random_quote(self, message, quotes):
        random_number = random.randint(0, (len(quotes) - 1))
        quote = str(quotes[random_number])
        if "by" not in quote:
            quote = "\"" + str(quotes[random_number]) + "\" - Taylor Swift"
        else:
            quote = "\"" + quote.replace("by ", "\" - ")
            return quote

    def add_quote(self, message):
        newQuote = message.content.split(" ", 1)[1].replace("\"", "")
        if "by" not in newQuote:
            return "Format: {Zitat} by {Autor}"
        quotes.append(newQuote)
        with open('quotes.json', 'w') as fp:
            json.dump(quotes, fp)
            return "added quote \"" + newQuote + "\" to quotes"

    def get_lyrics(self, message):
        url = ""
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
                    return lyrics


client = Bot()
client.run(TOKEN)
