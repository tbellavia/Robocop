import os
import discord
import re
from dotenv import load_dotenv
from robocop.err_messages import ErrorMessages
from robocop.channels import Channels
from urlextract import URLExtract


load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()


# FIXME need to modify channel triggering : 
# should not trigger two errors when forbidden channel error has been 
# handled before


class Robocop(discord.Client):
    async def on_ready(self):
        self.bot_id = 634850328545853460
        self.reserved_keywords = [
            "False", "class", "finally", "is", "return",
            "None", "continue", "for", "lambda", "try",
            "True", "def", "from", "nonlocal", "while",
            "and", "del", "global", "not", "with",
            "as", "elif", "if", "or", "yield",
            "assert", "else", "import", "pass",	 
            "break", "except", "in", "raise",
            "print", "len", "[", "]", "{", "}"
        ]
        print(f"{client.user} has connected to Discord!")

    def is_not_markdown(self, message):
        regex = re.compile(r"(`{3}(.|\n)*`{3})")
        if regex.match(message) is None:
            return True
        return False

    def is_not_ressource_message(self, message):
        extractor = URLExtract()
        if len(extractor.find_urls(message)) == 0:
            return True
        return False

    async def on_message(self, message):
        # The return statment is here to avoid triggering other alerts.
        for mention in message.mentions:
            if mention.id == self.bot_id:
                await message.channel.send(
                    f"Mes sincères salutations {message.author.mention}"
                )
                return

        if message.channel.id in Channels.FORBIDDEN_CHANNELS.value:
            if self.is_not_ressource_message(message.content):
                await message.author.send(
                    "{}. Voici une copie de ton message, en cas de faux positif, n'hésites pas à prévenir un modérateur.\nMessage : {}".format(ErrorMessages.INAPPROPRIATE_CHANNEL_RESSOURCES.value.replace("<PLACEHOLDER>", message.author.mention), message.content)
                )
                await message.delete()
                return

        if self.is_not_markdown(message.content):
            splitted_message = message.content.split()  
            counter = sum([splitted_message.count(keyword) for keyword in self.reserved_keywords])
            counter += sum([1 for keyword in self.reserved_keywords if keyword in splitted_message])

            if counter >= 5:
                if message.channel.id in Channels.CODE_CHANNELS.value:
                    await message.channel.send(
                        ErrorMessages.MARKDOWN_FAIL.value.replace('<PLACEHOLDER>', message.author.mention)
                    )
                    return
                else:
                    await message.channel.send(
                        ErrorMessages.INAPPROPRIATE_CHANNEL_CODE.value.replace('<PLACEHOLDER>', message.author.mention)
                    )
                    return

client = Robocop()
client.run(token)