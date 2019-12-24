import os
import discord
import re
from random import randint
from dotenv import load_dotenv
from robocop.err_messages import ErrorMessages
from robocop.channels import Channels
from robocop.log_objects import LogObject
from robocop.expressions import Expressions
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
        self.DELETE_LIMIT = 5
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

    async def write_log(self, message, content):
        channel = self.get_channel(Channels.LOGGER.value[0])
        await channel.send(
            content + "\n" + ("=" * 50)
        )
        
    async def show_man(self, channel):
        await channel.send(
            "NAME : Robocop\n\nCOMMANDS :\n - man \n - del message_number [filter]"
        )

    async def on_message(self, message):
        # The return statment is here to avoid triggering other alerts.

        # Show man
        if message.content.startswith("!man"):
            await self.show_man(message.channel)

        # Delete command
        if message.content.startswith("!del") and any(role.name == "Modérateur" for role in message.author.roles):
            try:
                number = int(message.content.split()[1])
            except:
                number = -1
                await message.channel.send(ErrorMessages.DELETE_INTEGER_FAIL.value.replace("<PLACEHOLDER>", message.author.mention))

            if number <= self.DELETE_LIMIT:
                logs = await message.channel.history(limit=number + 1).flatten()

                for log in logs:
                    print(f"Deleting => {log.content}")
                    await self.write_log(message, f"Motif : {LogObject.MODERATION_DELETE.value}\nAuteur de la supression : {message.author}\nAuteur du message : {log.author}\nContenu : {log.content[:1400]}")
                    await log.delete()
            else:
                await message.channel.send(f"{message.author.mention} Limite de supression dépassée.")

        # Salute
        for mention in message.mentions:
            if mention.id == self.bot_id:
                # salutes = Expressions.SALUTE.value
                # Commenting for XMAS celebrationm replacing messages by xmas expressions
                salutes = Expressions.XMAS_SALUTE.value
                await message.channel.send(
                    f"{salutes[randint(0, len(salutes) - 1)]} {message.author.mention}"
                )
                return

        # Forbidden channel
        if message.channel.id in Channels.FORBIDDEN_CHANNELS.value:
            if self.is_not_ressource_message(message.content):
                await message.author.send(
                    "{}. Voici une copie de ton message, en cas de faux positif, n'hésites pas à prévenir un modérateur.\nMessage : {}".format(ErrorMessages.INAPPROPRIATE_CHANNEL_RESSOURCES.value.replace("<PLACEHOLDER>", message.author.mention), message.content[:1000])
                )
                await self.write_log(message, f"Motif : {LogObject.BAD_RESSOURCE.value}\nAuteur : {message.author}\nContenu : {message.content[:1000]}")
                await message.delete()
                return

        # Markdown fail
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
