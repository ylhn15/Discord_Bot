# Discord_Bot
Discord Bot written in Python with the Discord API.

## Running the bot
Create a bot on the official discord developer page and add it to your server.

https://discordapp.com/developers/applications/

Create a config.json file and add the token of the bot in the following format:
`
{"token" : TOKEN}
`

Start the python script on your device.

### Dependencies
Run 
* `pip3 install google --user`
* `pip3 install discord --user`
to install the necessary packages.

## Commands
* `!(l)yrics {title}` - Searches for the given title on songtexte.com and returns the lyrics, if available.
* `!(q)uote` - Returns a random quote from the quotes.json file.
* `!(q)uoteWithId/!qi {ID}` - Returns the quote with the specified ID from the quotes.json file.
* `!addQuote/!aq {Quote} by {Author}` - Adds a quote to the quotes.json - the format is `{Quote} by {Author}`.
* `!deleteQuote/!dq {ID}` - Deletes the quote with the specified ID from the quotes.json file.
* `!code {Pythoncode}` Write your own little script directly in Discord.
* `!run` Run your script.
* `!debug` Returns the code of your script.
* `!(h)elp` - Returns this command list

