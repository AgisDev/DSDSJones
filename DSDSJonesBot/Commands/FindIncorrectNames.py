import discord

async def findIncorrectNames(client, messageObj):
    ckRole = discord.utils.get(messageObj.channel.guild.roles, name="Crimson Knight")
    
    for detectedMember in messageObj.channel.guild.members:
        
        if ckRole in detectedMember.roles:
            
            splitName = detectedMember.display_name.split(", ")
            if len(splitName) != 2:
                await messageObj.reply(f'{detectedMember.display_name} | {detectedMember.name} | {detectedMember.mention}')
            else:
                if splitName[0][0].isupper() == False or splitName[1][0].isupper() == False:
                    await messageObj.reply(f'{detectedMember.display_name} | {detectedMember.name} | {detectedMember.mention}')
                
    await messageObj.reply("Name check concluded.")                	
            