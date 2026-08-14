import discord
import os
import ipaddress
import socket

from library.minecraft import serverstat
from library.minecraft import base64toimg

from discord import app_commands
from discord.ext import commands
from discord.app_commands import Choice


def is_blocked_ip(ip: str) -> bool:
    addr = ipaddress.ip_address(ip)

    return (
        addr.is_private
        or addr.is_loopback
        or addr.is_link_local
        or addr.is_reserved
        or addr.is_multicast
    )


def is_blocked_address(hostname: str) -> bool:
    try:
        results = socket.getaddrinfo(
            hostname,
            None,
            type=socket.SOCK_STREAM
        )

        for result in results:
            ip = result[4][0]

            if is_blocked_ip(ip):
                return True

        return False
    except socket.gaierror:
        return False


def setup(bot: commands.bot.Bot):
    @bot.tree.command(name="pingmc", description="Ping Java Or Bugrock Minecraft Server!")
    @app_commands.allowed_installs(
        guilds=True,
        users=True
    )
    @app_commands.allowed_contexts(
        guilds=True,
        dms=True,
        private_channels=True
    )
    @app_commands.choices(
        server=[
            Choice(name="Bedrock Server", value="b"),
            Choice(name="Java Server", value="j")
        ]
    )
    async def pingmc(interaction: discord.Interaction, server: str, address: str, port: int = None):
        await interaction.response.defer()

        if is_blocked_address(str(address)):
            await interaction.followup.send("Sorry But That IP Is Blocked For Pinging")

            return

        embed = None
        res = None
        file = None
        icon_path = None

        if server == "j":
            info = None

            if port is None:
                info = serverstat.PingJavaServer(address)
            else:
                info = serverstat.PingJavaServer(address, port)

            data = info.get("data")

            if info.get("online") == False:
                res = f"Unable To Connect To Server As\n```py\n{data.get("error")}\n```"
            else:
                icon_path = base64toimg.ConvertB64AndGiveMePath(data.get("b64icon"))

                embed = discord.Embed(
                    color=discord.colour.Colour.blue(),
                    title="Java Server Info",
                    description=f"At: {str(data.get("where").get("ip"))} | Port: {str(data.get("where").get("port"))}"
                )
                embed.add_field(name="MOTD", value=f"```mc\n{data.get("motd")}\n```")
                embed.add_field(name="Playing", value=f"{str(data.get("players").get("online"))} Out Of {str(data.get("players").get("limit"))}", inline=False)
                embed.add_field(name="Ping", value=f"{str(data.get("ping"))}ms", inline=False)
                embed.add_field(name="Software/Version", value=f"{str(data.get("ver"))}", inline=True)
                
                if icon_path:
                    file = discord.File(fp=icon_path, filename="icon.png")
                    embed.set_thumbnail(url="attachment://icon.png")
                else:
                    embed.set_thumbnail(url="https://prayoadmii.neocities.org/Assets/CDN/minecraft/unknown_server.png")
        elif server == "b":
            info = None

            if port is None:
                info = serverstat.PingBedrockServer(address)
            else:
                info = serverstat.PingBedrockServer(address, port)
            
            data = info.get("data")
            
            if info.get("online") == False:
                res = f"Unable To Connect To Server As\n```py\n{data.get("error")}\n```"
            else:
                embed = discord.Embed(
                    color=discord.colour.Colour.gold(),
                    title="Bedrock Server Info",
                    description=f"At: {str(data.get("where").get("ip"))} | Port: {str(data.get("where").get("port"))}"
                )
                embed.add_field(name="MOTD", value=f"```mc\n{data.get("motd")}\n```")
                embed.add_field(name="Playing", value=f"{str(data.get("players").get("online"))} Out Of {str(data.get("players").get("limit"))}", inline=False)
                embed.add_field(name="Ping", value=f"{str(data.get("ping"))}ms", inline=True)
                embed.add_field(name="Software/Version", value=str(data.get("ver")), inline=False)
                embed.add_field(name="Gamemode", value=str(data.get("gamemode")), inline=True)
                embed.add_field(name="World Name", value=str(data.get("world")), inline=True)
        
        if file:
            await interaction.followup.send(content=res, embed=embed, file=file)
        else:
            await interaction.followup.send(content=res, embed=embed)
        
        if icon_path:
            os.remove(icon_path)