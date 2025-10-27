import discord
from discord.ext import commands
from discord import app_commands


class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reaction_role_map = {}
        self.GUILD_ID_FALLBACK = 1424859449331552298  # Replace with your server ID

    @app_commands.command(
        name="reactionroles",
        description="Set up reaction roles for your last sent message.",
    )
    @app_commands.describe(
        emojis="Comma-separated list of emojis (ex. 😀,🔥,💀)",
        roles_str="Comma-separated list of role names (ex. Software,Mechanical,Composites)",
    )
    async def reactionroles(
        self, interaction: discord.Interaction, emojis: str, roles_str: str
    ):
        await interaction.response.defer(ephemeral=True)

        # get emojis and roles
        emoji_list = [e.strip() for e in emojis.split(",")]
        role_names = [r.strip() for r in roles_str.split(",")]

        # # interaction.guild
        # interaction.guild = self.bot.get_guild(1424859449331552298)

        guild = interaction.guild or self.bot.get_guild(self.GUILD_ID_FALLBACK)
        if guild is None:
            await interaction.response.send_message(
                "This command must be used in a server (not in DMs).", ephemeral=True
            )
            return

        roles = []
        for role in role_names:
            found_role = discord.utils.get(guild.roles, name=role)
            if not found_role:
                await interaction.followup.send(
                    f"Role '{role}' not found in this server.", ephemeral=True
                )
                return
            roles.append(found_role)

        if len(emoji_list) != len(roles):
            await interaction.followup.send(
                "Number of emojis must match number of roles.", ephemeral=True
            )
            return

        channel = interaction.channel

        if channel is None or not isinstance(channel, discord.TextChannel):
            await interaction.followup.send("somethings wong", ephemeral=True)
            return

        target_message = None

        # get the users last message
        async for msg in channel.history(limit=50):
            if msg.author == interaction.user:
                target_message = msg
                break
        else:
            await interaction.followup.send(
                "Couldn't find one of your recent messages in this channel.",
                ephemeral=True,
            )
            return

        # Add reactions to the message
        for emoji in emoji_list:
            try:
                await target_message.add_reaction(emoji)
            except discord.HTTPException:
                await interaction.followup.send(
                    f"⚠️ Could not add reaction {emoji}. Skipping.", ephemeral=True
                )

        # Save mapping
        self.reaction_role_map[target_message.id] = dict(zip(emoji_list, roles))

        await interaction.followup.send("✅ Reaction roles configured!")

    async def cog_load(self):
        guild = discord.Object(id=1424859449331552298)
        self.bot.tree.add_command(self.reactionroles, guild=guild)
        print("✅ Reaction role command added!")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):  # when a user reacts
        if payload.message_id not in self.reaction_role_map:
            print("Message ID not in reaction role map on add")
            return

        emoji = str(payload.emoji)
        role = self.reaction_role_map[payload.message_id].get(emoji)
        if not role:
            return

        if role:
            member = payload.member
            if member:
                await member.add_roles(role)
                print(f"Added {role.name} to {member.name}")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):  # when a user removes their react
        if payload.message_id not in self.reaction_role_map:
            print("Message ID not in reaction role map on remove")
            return

        guild = self.bot.get_guild(payload.guild_id)
        emoji = str(payload.emoji)
        role = self.reaction_role_map[payload.message_id].get(emoji)
        if not role:
            return

        # role = discord.utils.get(guild.roles, name=role_name)
        if role:
            member = guild.get_member(payload.user_id)
            if member:
                await member.remove_roles(role)
                print(f"Removed {role.name} from {member.name}")
