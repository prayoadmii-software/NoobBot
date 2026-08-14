import discord
import asyncio

from library.core.helpmodule import textfilter
from library.core.helpmodule import noping

from discord import app_commands
from discord.ext import commands

def clean_ping(data: str, interaction: discord.Integration) -> str:
    output = "..."

    ping_res = noping.check(data)

    if ping_res == 1 or ping_res == 2:
        output = f"AYO {interaction.user.mention}!\nI'M NOT GONNA PING ANYONE!!!"
    elif ping_res == 3:
        output = f"AYO {interaction.user.mention}!\nI'M NOT PINGING ANY ROLES!!!"
    else:
        output = data
    
    return output

def setup(bot: commands.bot.Bot):
    @bot.tree.command(
        name="prayoadmiistyle",
        description="Turn Your Messages Into PrayoadMii Style (Filtered Needed!)"
    )
    @app_commands.allowed_installs(
        guilds=True,
        users=True
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=True,
        private_channels=True
    )
    async def prayoadmiistyle(interaction: discord.Interaction, message: str):
        await interaction.response.defer()

        filtered_message = await asyncio.to_thread(
            textfilter.FilterStringAsync,
            message
        )
        
        cleaned = clean_ping(filtered_message, interaction)

        transformed_message = ' '.join(word.capitalize() for word in cleaned.split())

        await interaction.followup.send(str(transformed_message).replace("\\n", "\n"))


    @bot.tree.command(
        name="filter",
        description="Filter The Bad Words Out From Your Message Text"
    )
    @app_commands.allowed_installs(
        guilds=True,
        users=True
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=True,
        private_channels=True
    )
    async def filter_cmd(interaction: discord.Interaction, message: str):
        await interaction.response.defer(ephemeral=True)

        filtered_message = await asyncio.to_thread(
            textfilter.FilterStringAsync,
            message
        )
        
        cleaned = clean_ping(filtered_message, interaction)

        await interaction.followup.send(str(cleaned).replace("\\n", "\n"), ephemeral=True)


    @bot.tree.command(
        name="echo",
        description="Make Bot Say Anything You Want! (Filtered First)"
    )
    @app_commands.allowed_installs(
        guilds=True,
        users=True
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=True,
        private_channels=True
    )
    async def say(interaction: discord.Interaction, message: str):
        await interaction.response.defer()

        filtered_message = await asyncio.to_thread(
            textfilter.FilterStringAsync,
            message
        )

        cleaned = clean_ping(filtered_message, interaction)

        await interaction.followup.send(str(cleaned).replace("\\n", "\n"))