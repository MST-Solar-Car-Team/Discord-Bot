import discord
from discord.ext import commands
from cogs.ping import Greetings
import os
import sys

token = os.getenv("DISCORD_BOT_TOKEN")

if token is None:
    print("DISCORD_BOT_TOKEN is not set")
    sys.exit(1)


class DiscordBot(commands.Bot):
    async def setup_hook(self) -> None:
        bot.status = discord.Status.online
        await self.setup_cogs()

    async def setup_cogs(self) -> None:
        await bot.add_cog(Greetings(self))


intents = discord.Intents.default()
intents.message_content = True
bot = DiscordBot(command_prefix="!", intents=intents)

bot.status = discord.Status.online

bot.run(token)
