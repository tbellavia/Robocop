import os
import discord
import re
from dotenv import load_dotenv
from robocop.err_messages import ErrorMessages

load_dotenv()
token = os.getenv('DISCORD_TOKEN')

client = discord.Client()



class Robocop(discord.Client):
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
        self.code_channels = [
            "aide-python", "aide-autres-langages", 
            "aide-web", "aide-vfx", 
            "différences-entre-versions", "tutorat",
            "aide-datascience", "projets-datascience",
            "machine-learning", "deep-learning",
            "la-formation-complète-python", "interface-graphiques-avec-pyside"
        ]
        print(f"{client.user} has connected to Discord!")

    async def on_message(self, message):
        regex = re.compile(r"(`{3}(.|\n)*`{3})")

        if regex.match(message.content) is None:
            splitted_message = message.content.split()
            counter = sum([splitted_message.count(keyword) for keyword in self.reserved_keywords])
            counter += sum([1 for keyword in self.reserved_keywords if keyword in splitted_message])

            if counter >= 5:
                if message.channel in self.code_channels:
                    await message.channel.send(
                        f"{ErrorMessages.INAPPROPRIATE_CHANNEL_CODE.value.replace('<PLACEHOLDER>', message.author.mention)}"
                    )
                else:
                    await message.channel.send(
                        f"{ErrorMessages.MARKDOWN_FAIL.value.replace('<PLACEHOLDER>', message.author.mention)}"
                    )

client = Robocop()
client.run(token)