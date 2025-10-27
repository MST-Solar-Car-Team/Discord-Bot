import discord
from discord.ext import commands

from cogs.slash_reaction_roles import ReactionRoles

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
        self.add_listener(self.on_ready)

    async def setup_cogs(self) -> None:
        await self.add_cog(ReactionRoles(self))

    async def on_ready(self):
        await self.tree.sync(guild=discord.Object(id=1424859449331552298))


intents = discord.Intents.default()
intents.message_content = True
intents.reactions = True
intents.members = True
bot = DiscordBot(command_prefix="!", intents=intents)

bot.status = discord.Status.online

bot.run(token)
