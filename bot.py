import json
import os
import discord
import random
import urllib.request
import googlesearch
from bs4 import BeautifulSoup


class Bot(discord.Client):
    with open('quotes.json') as json_file:
        try:
            quotes = json.load(json_file)
        except ValueError:
            quotes = []

    async def on_message(self, message):
        keyword = message.content.split(" ", 1)[0]
        if message.author == client.user:
            return
        if keyword == '!help' or keyword == '!h':
            help_msg = open('helpmessage.txt', 'r').read()
            await message.channel.send(help_msg + "\n https://github.com/ylhn15/Discord_Bot")
        if keyword == '!quote' or keyword == '!q':
            await message.channel.send(self.get_random_quote(message, self.quotes))
        if keyword == '!quoteWithId' or keyword == '!qi':
            await message.channel.send(self.get_quote_by_id(message, self.quotes))
        if keyword == '!deleteQuote' or keyword == '!dq':
            await message.channel.send(self.delete_quote_by_id(message, self.quotes))
        if keyword == '!lyrics' or keyword == '!l':
            searchterm = message.content.split(" ", 1)
            if len(searchterm) > 1:
                await message.channel.send("Suche nach " + searchterm[1])
            else:
                await message.channel.send("Suchbegriff eingeben")
                return
            lyrics = self.get_lyrics(searchterm)
            if lyrics is None:
                await message.channel.send("Fehler: Songtext konnte nicht gefunden werden")
            await self.split_message(message, lyrics, 1999)
        if keyword == '!addQuote' or keyword == '!aq':
            await message.channel.send(self.add_quote(message))
        if  message.content.startswith('!code'):
            self.write_code(message)
            await message.channel.send("Code written...")
        if keyword == '!run':
            await self.split_message(message, self.run_code(message), 1995, isCode=True)
        if keyword == '!debug':
            await message.channel.send("`" + self.read_code(message) + "`")
        if keyword == '!contribute':
            await message.channel.send("https://github.com/ylhn15/Discord_Bot")

    async def on_ready(self):
        print('Logged in as')
        print(client.user.name)
        print(client.user.id)
        print('------')

    async def split_message(self, message, output, max_chunk_size, isCode = None):
            chunks = ([output[i: i + max_chunk_size] for i in range(0, len(output), max_chunk_size)])
            for text in chunks:
                if isCode is True:
                    await message.channel.send("`" + text + "`")
                else:
                    await message.channel.send(text)

    def get_filename(self, message):
        filename = message.content.split(' ', 1)[1]
        filename = filename.split('\n', 1)[0]
        return filename

    def write_code(self, message):
        filename = self.get_filename(message)
        # test = message.content.split("\n", 2)[2].replace("`", "")
        code = "import sys \nsys.stdout = open('output', 'w') \n"
        code = code + message.content.split('\n', 1)[1].replace('`', '')
        code = code + '\n'
        output = open(filename, 'w')
        output.write(code)

    def run_code(self, message):
        filename = self.get_filename(message)
        os.system("python3 " + filename)
        return self.read_output()

    def read_code(self, message):
        filename = self.get_filename(message)
        output = open(filename, 'r')
        return output.read()

    def read_output(self):
        output = open('output', 'r')
        return output.read()

    def get_random_quote(self, message, quotes):
        if len(self.quotes) == 0:
            return "No quotes available"
        else:
            random_number = random.randint(0, (len(self.quotes) - 1))
            quote = quotes[random_number]
            return quote['quote'] + " - " + quote['author']

    def get_quote_by_id(self, message, quotes):
        quoteId = message.content.split(" ",1)[1]
        print(quoteId)
        for quote in quotes:
            if quote['id'] == int(quoteId):
                return quote['quote'] + " - " + quote['author']
        return "Quote not found"

    def add_quote(self, message):
        if len(self.quotes) > 0:
            lastQuote = self.quotes[len(self.quotes) - 1]
            try:
                lastId = int(lastQuote['id']) + 1
            except KeyError:
                lastId = 0
        else:
            lastId = 0
        newQuote = message.content.split(' ', 1)[1].replace('\"', '')
        if 'by' not in newQuote:
            return "Format: {Zitat} by {Autor}"
        quote = {
            "id" : lastId,
            "author" : newQuote.split("by", 1)[1],
            "quote" : newQuote.split("by", 1)[0]
        }
        self.quotes.append(quote)
        with open('quotes.json', 'w') as fp:
            json.dump(self.quotes, fp)
            return "added quote \"" + newQuote + "\" to quotes with id " + str(lastId)

    def delete_quote_by_id(self, message, quotes):
        quoteId = message.content.split(" ",1)[1]
        print(quoteId)
        for quote in quotes:
            if quote['id'] == int(quoteId):
                with open('quotes.json', 'w') as fp:
                    quotes.remove(quote)
                    json.dump(self.quotes, fp)
                    return "removed quote with id: " + quoteId
        return "Quote not found"

    def get_lyrics(self, searchterm):
        url = ''
        for text in  searchterm:
            url += text
            url += ' '
            url += 'lyrics'
        search_results = googlesearch.search(url, stop=100)
        for result in search_results:
            if 'songtexte.com' in result:
                print(result)
                if len(result) > 0:
                    page = urllib.request.urlopen(result)
                    soup = BeautifulSoup(page.read(), 'html.parser')
                    lyrics = soup.find(id='lyrics').get_text()
                    return lyrics

    def getBotToken(self):
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
            return data['token']



client = Bot()
client.run(client.getBotToken())
