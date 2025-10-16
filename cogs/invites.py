from typing import Dict, List, Optional, Tuple
from discord import Invite, Member, Interaction, Role
from discord.abc import GuildChannel
from discord.app_commands import command, guilds, describe
from discord.ext.commands import Cog, Bot
from config import SOLAR_CAR_GUILD, SOLAR_CAR_GUILD_ID


class Invites(Cog):
    def __init__(self, bot):
        self.bot: Bot = bot
        # This will cause a memory leak if too many invites expire instead of being deleted?
        # Invite code as KEY, number of uses as Value
        self.invites: Dict[str, int] = {}
        self.invite_roles: Dict[str, Role] = {}

    def invites_to_dict(self, invites: List[Invite]) -> Dict[str, int]:
        new_dict: Dict[str, int] = {}
        for invite in invites:
            new_dict[invite.code] = invite.uses or 0
        return new_dict

    # Returns a tuple with what invite link was added and its current increment
    # Also updates the dictonary in self to reflect new changes
    def process_invite_change(
        self, new_invites: List[Invite]
    ) -> Optional[Tuple[str, int]]:
        for invite in new_invites:
            uses = invite.uses or 0
            if self.invites[invite.code] != uses:
                self.invites = self.invites_to_dict(new_invites)
                return (invite.code, uses)

    @Cog.listener()
    async def on_invite_create(self, invite: Invite):
        self.invites[invite.code] = Invite.uses or 0

    @Cog.listener()
    async def on_invite_delete(self, invite: Invite):
        self.invites.pop(invite.code)

    @Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(SOLAR_CAR_GUILD_ID)
        if guild:
            self.invites = self.invites_to_dict(await guild.invites())

    @Cog.listener()
    async def on_member_join(self, member: Member):
        join_details = self.process_invite_change(await member.guild.invites())
        if join_details and join_details[0] in self.invite_roles:
            await member.add_roles(
                self.invite_roles[join_details[0]],
                reason="Automatically added by join link",
            )

    @command(
        name="create_join_link",
        description="Creates a join link with a role assigned to it",
    )
    @guilds(SOLAR_CAR_GUILD)
    @describe(
        join_role="A role to apply to users joining using this link",
        channel="The channel the invite is linked to",
    )
    async def create_join_link(
        self, interaction: Interaction, channel: GuildChannel, join_role: Role
    ):
        guild = interaction.guild
        if guild:
            invite = await channel.create_invite()
            self.invite_roles[invite.code] = join_role
            await interaction.response.send_message(
                ephemeral=True, content=f"Invite code: {invite.code}"
            )
