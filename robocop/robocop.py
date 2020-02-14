import discord
import logging
import re
import os
import json

from random import randint
from urlextract import URLExtract

from robocop.err_messages import ErrorMessages
from robocop.log_objects import LogObject
from robocop.expressions import Expressions

# LOGGER SETUP
logger = logging.getLogger()
logger.setLevel("INFO")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s (line %(lineno)s in %(pathname)s)', datefmt='%d/%m/%Y %H:%M:%S')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


class Channels:
    def __init__(self, staging=True):
        super().__init__()
        filename = "channels-staging.json" if staging == 1 else "channels.json"
        path = os.path.join(os.path.abspath(os.path.dirname(__file__)), filename)

        values = {}
        if os.path.exists(path) and os.path.isfile(path):
            with open(path, "r") as f:
                values = json.load(f)

        self.text_channels = values.get("TEXT_CHANNELS", [])
        self.log_channel = values.get("LOG_CHANNEL", [])[0]
        self.forbidden_channels = values.get("FORBIDDEN_CHANNELS", [])


class Robocop(discord.Client):
    def __init__(self, staging=True):
        super().__init__()
        self.staging = staging

    async def on_ready(self):
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
        self.channels = Channels(staging=self.staging)
        logging.info(f"{self.user} has connected to Discord!")

    def is_not_markdown(self, message):
        regex = re.compile(r"(`{3}(.|\n)*`{3})")
        if regex.search(message) is None:
            return True
        return False

    def is_not_ressource_message(self, message):
        extractor = URLExtract()
        if len(extractor.find_urls(message)) == 0:
            return True
        return False

    async def write_log(self, message, content):
        channel = self.get_channel(self.channels.log_channel)
        await channel.send(content + "\n" + ("=" * 50))

    async def show_man(self, channel):
        await channel.send("NAME : Robocop\n\nCOMMANDS :\n - man \n - del message_number [filter]")

    async def on_message(self, message):
        # The return statment is here to avoid triggering other alerts.

        # Show man
        if message.content.startswith("!man"):
            logger.info("Manual asked. Showing all commands.")
            await self.show_man(message.channel)

        # Delete command
        elif message.content.startswith("!del") and any(role.name == "Modérateur" for role in message.author.roles):
            logger.info("Deleting messages...")
            try:
                number = int(message.content.split()[1])
            except:
                number = -1
                logger.info("Couldn't delete message. Please pass a valid number of messages to delete (integer).")
                await message.channel.send(ErrorMessages.DELETE_INTEGER_FAIL.value.replace("<PLACEHOLDER>", message.author.mention))

            if number <= self.DELETE_LIMIT:
                logs = await message.channel.history(limit=number + 1).flatten()

                for log in logs:
                    logger.info(f"Deleting => {log.content}")
                    await self.write_log(message,
                                         f"Motif : {LogObject.MODERATION_DELETE.value}\nAuteur de la supression : {message.author}\nAuteur du message : {log.author}\nContenu : {log.content[:1400]}")
                    await log.delete()
            else:
                await message.channel.send(f"{message.author.mention} Limite de supression dépassée.")

        # Salute
        elif len([mention for mention in message.mentions if mention.id == self.user.id]) != 0:
            salutes = Expressions.SALUTE.value
            await message.channel.send(
                    f"{salutes[randint(0, len(salutes) - 1)]} {message.author.mention}"
            )

        # Forbidden channel
        elif message.channel.id in self.channels.forbidden_channels:
            if self.is_not_ressource_message(message.content):
                await message.author.send(
                        "{}. Voici une copie de ton message, en cas de faux positif, n'hésites pas à prévenir un modérateur.\nMessage : {}".format(
                                ErrorMessages.INAPPROPRIATE_CHANNEL_RESSOURCES.value.replace("<PLACEHOLDER>", message.author.mention), message.content[:1000])
                )
                await self.write_log(message, f"Motif : {LogObject.BAD_RESSOURCE.value}\nAuteur : {message.author}\nContenu : {message.content[:1000]}")
                await message.delete()

        # Markdown fail
        elif self.is_not_markdown(message.content):
            splitted_message = message.content.split()
            counter = sum([splitted_message.count(keyword) for keyword in self.reserved_keywords])
            counter += sum([1 for keyword in self.reserved_keywords if keyword in splitted_message])

            if counter >= 5:
                if message.channel.id in self.channels.text_channels:
                    await message.channel.send(
                            ErrorMessages.MARKDOWN_FAIL.value.replace('<PLACEHOLDER>', message.author.mention)
                    )
                    return
                else:
                    await message.channel.send(
                            ErrorMessages.INAPPROPRIATE_CHANNEL_CODE.value.replace('<PLACEHOLDER>', message.author.mention)
                    )
                    return
