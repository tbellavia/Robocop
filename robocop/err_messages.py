from enum import Enum

class ErrorMessages(Enum):
    INAPPROPRIATE_CHANNEL_CODE = "Woops, <PLACEHOLDER> on dirait que tu t'es trompé de channel. Si tu veux poster du code, je te conseille de regarder dans les salons appropriés qui te conviendront mieux tels que"
    INAPPROPRIATE_CHANNEL_RESSOURCES = "Woops, <PLACEHOLDER> on dirait que tu t'es trompé de channel. Si tu veux poster autre choses que des ressources, je t'invite à explorer de nouvelles contrées."
    MARKDOWN_FAIL = "Hey mon vieux, <PLACEHOLDER> si tu veux poster du code tu peux le mettre en markdown c'est jolie et ça facilite le travail de compréhension de ton interlocuteur, check moi donc un peu ça <https://support.discordapp.com/hc/fr/articles/210298617-Bases-de-la-mise-en-forme-de-texte-Markdown-mise-en-forme-du-chat-gras-italique-soulign%C3%A9->"