import os
from dotenv import load_dotenv
from robocop import robocop

# GET ENVIRONMENT VARIABLES
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
STAGING = os.getenv("STAGING") == 'True'

if __name__ == "__main__":
    client = robocop.Robocop(staging=STAGING)
    client.run(TOKEN)
