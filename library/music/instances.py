from library.music.player import MusicPlayer
from library.core import console

players = {}

def get_player(guild, bot):
    if guild.id not in players:
        players[guild.id] = MusicPlayer(guild, bot)
    
    return players[guild.id]