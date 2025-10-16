from discord import Status, Intents
from discord.ext import commands
from cogs.invites import Invites
from config import TOKEN, SOLAR_CAR_GUILD


class DiscordBot(commands.Bot):
    async def setup_hook(self) -> None:
        await self.setup_cogs()
        self.add_listener(self.on_ready)

    async def setup_cogs(self) -> None:
        # await bot.add_cog(Greetings(self))
        await self.add_cog(Invites(self))

    async def on_ready(self):
        print("bot is ready!")
        await self.tree.sync(guild=SOLAR_CAR_GUILD)


intents = Intents.default()
intents.invites = True
intents.members = True
bot = DiscordBot(command_prefix=[], intents=intents)

bot.run(TOKEN)
bot.status = Status.online
