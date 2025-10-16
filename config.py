from discord import Object
import os

TOKEN_RAW = os.getenv("DISCORD_BOT_TOKEN")
SOLAR_CAR_GUILD_ID_RAW = os.getenv("DISCORD_BOT_GUILD")

assert SOLAR_CAR_GUILD_ID_RAW is not None, "DISCORD_BOT_GUILD is not set"
SOLAR_CAR_GUILD: Object = Object(SOLAR_CAR_GUILD_ID_RAW)
SOLAR_CAR_GUILD_ID: int = int(SOLAR_CAR_GUILD_ID_RAW)

assert TOKEN_RAW is not None, "DISCORD_BOT_TOKEN is not set"
TOKEN: str = TOKEN_RAW
