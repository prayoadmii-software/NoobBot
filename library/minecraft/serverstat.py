import re

from mcstatus import BedrockServer, JavaServer

def CleanMineText(text: str):
    return re.sub(r"§.", "", text)

def PingBedrockServer(address: str, port: int = 19132):
    try:
        server = BedrockServer.lookup(f"{str(address)}:{str(port)}")
        stat = server.status()

        pack = {
            "online": True,
            "data": {
                "motd": CleanMineText(str(stat.description)),
                "players": {
                    "online": int(stat.players.online),
                    "limit": int(stat.players.max)
                },
                "ping": int(stat.latency),
                "gamemode": CleanMineText((str(stat.gamemode))),
                "ver": CleanMineText(str(stat.version.name)),
                "world": CleanMineText(str(stat.map_name)),
                "where": {
                    "ip": str(address),
                    "port": int(port)
                }
            }
        }

        return pack
    except Exception as e:
        pack = {
            "online": False,
            "data": {
                "error": str(e)
            }
        }

        return pack

def PingJavaServer(address: str, port: int = 25565):
    try:
        server = JavaServer.lookup(f"{str(address)}:{str(port)}")
        stat = server.status()
        
        pack = {
            "online": True,
            "data": {
                "motd": CleanMineText(str(stat.description)),
                "players": {
                    "online": int(stat.players.online),
                    "limit": int(stat.players.max)
                },
                "ping": int(stat.latency),
                "ver": CleanMineText(str(stat.version.name)),
                "b64icon": str(stat.icon) if stat.icon else None,
                "where": {
                    "ip": str(address),
                    "port": int(port)
                }
            }
        }

        return pack
    except Exception as e:
        pack = {
            "online": False,
            "data": {
                "error": str(e)
            }
        }

        return pack