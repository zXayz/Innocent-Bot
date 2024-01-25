from __future__ import annotations
import discord
from discord.ext import commands
from typing import Any
import traceback

class BasicPaginator(discord.ui.View):
    def __init__(
                self, 
                ctx: commands.Context, 
                *,
                embeds: dict[discord.Embed], 
                timeout: float = 180):
        
        super().__init__(timeout=timeout)
        self.response: Any = None
        self.ctx = ctx
        self.embeds: dict[discord.Embed] = embeds
        self.curren_page: int = 1
        self.max_page: int = len(embeds)


    async def on_timeout(self) -> None:
        self.stop()
        if self.response:
            await self.response.edit(view=None)

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user and interaction.user.id in (
            self.ctx.bot.owner_id,
            self.ctx.author.id,
        ):
            return True
        await interaction.response.send_message(
            "This menu cannot be controlled by you, sorry!", ephemeral=True
        )
        return False
    
    
    async def on_error(
        self, interaction: discord.Interaction, error: Exception, item: discord.ui.Item
    ) -> None:
        if interaction.response.is_done():
            await interaction.followup.send(
                "An unknown error occurred, sorry", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "An unknown error occurred, sorry", ephemeral=True
            )

        try:
            exc = "".join(
                traceback.format_exception(
                    type(error), error, error.__traceback__, chain=False
                )
            )
            embed = discord.Embed(
                title=f"{self.source.__class__.__name__} Error",
                description=f"```py\n{exc}\n```",
                timestamp=interaction.created_at,
                colour=0xCC3366,
            )
            embed.add_field(
                name="User", value=f"{interaction.user} ({interaction.user.id})"
            )
            embed.add_field(
                name="Guild", value=f"{interaction.guild} ({interaction.guild_id})"
            )
            embed.add_field(
                name="Channel",
                value=f"{interaction.channel} ({interaction.channel_id})",
            )
            await self.ctx.bot.stats_webhook.send(embed=embed)
        except discord.HTTPException:
            pass
        

    @discord.ui.button(
        label=f"Prev",
        style=discord.ButtonStyle.primary,
    )
    async def first_callback_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        pass


    @discord.ui.button(
        label=f"Jump To",
        style=discord.ButtonStyle.primary,
    )
    async def second_callback_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        pass


    @discord.ui.button(
        label=f"Next",
        style=discord.ButtonStyle.primary,
    )
    async def third_callback_button(
        self, interaction: discord.Interaction, button: discord.ui.Button
    ):
        await interaction.response.defer()
        pass



