import discord
import json




async def logMessageToLeaderboard(client, messageObj):
    leaderboardStatsFile = None
    leaderboardStatsDict = None
    
    leaderboardStatsFile = open("Resources/ChatLeaderboard.json", "r")
    
    try:
        leaderboardStatsDict = json.load(leaderboardStatsFile)
    except:
        leaderboardStatsDict = {}
        
    leaderboardStatsFile.close()
    
    
    if messageObj.author.display_name in leaderboardStatsDict:
        leaderboardStatsDict[messageObj.author.display_name] = leaderboardStatsDict[messageObj.author.display_name] + 1
    else:
        leaderboardStatsDict[messageObj.author.display_name] = 1
        
    
    leaderboardStatsFile = open("Resources/ChatLeaderboard.json", "w")
    json.dump(leaderboardStatsDict, leaderboardStatsFile, indent=4)
    
    
    

async def displayLeaderboard(client, messageObj):
    leaderboardStatsFile = open("Resources/ChatLeaderboard.json", "r")
    
    try:
        leaderboardStatsDict = json.load(leaderboardStatsFile)
    except:
        leaderboardStatsDict = {}
        
    leaderboardStatsFile.close()
    
    if len(leaderboardStatsDict) == 0:
        return
    
    embed = discord.Embed(title="Server chat leaderboard:")
    
    leader = None
    
    leaderList = {}
    
    for i in range(1,6):
        if len(leaderboardStatsDict)>0:
            
            leader = max(leaderboardStatsDict, key=leaderboardStatsDict.get)
            leaderList[i] = {}
            leaderList[i][leader] = leaderboardStatsDict[leader]
            del leaderboardStatsDict[leader]
            
            ex = {
                1 : {
                    "Leader" : 1
                }
            }
            
            leader = None
        
    for i in range(1, len(leaderList)+1):
        embed.add_field(name=f'{i}. {list(leaderList[i].keys())[0]}', value=f'{leaderList[i][list(leaderList[i].keys())[0]]} messages.', inline=False)
        
        
    await messageObj.channel.send("", embed=embed)
        
        
    
    
    