from library.music.player import MusicPlayer
from prayoadmii_lib import console

players = {}

def get_player(guild, bot):
    if guild.id not in players:
        players[guild.id] = MusicPlayer(guild, bot)
    
    return players[guild.id]