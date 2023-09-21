import discord


async def logDeletedMessage(client, deletedMessageObj):
    if deletedMessageObj.author == client.user:
        return
    
    embed = discord.Embed(title="Deleted message event.", colour=0x00ff1e)
    embed.add_field(name="User who deleted the message:", value=(f'{deletedMessageObj.author.name} | {deletedMessageObj.author.display_name}'), inline=False)
    embed.add_field(name="The channel the message was sent in:", value=deletedMessageObj.channel.name, inline=False)
    embed.add_field(name="What the deleted message said:", value=deletedMessageObj.content, inline=False)
    
    if deletedMessageObj.attachments:
        if len(deletedMessageObj.attachments) == 1:
            if deletedMessageObj.attachments[0].url.endswith(('.jpg', '.png', '.jpeg', '.gif')):
                new_url = deletedMessageObj.attachments[0].url.replace('cdn.discordapp.com', 'media.discordapp.net')
                embed.set_image(url=new_url)
            else:
                new_url = deletedMessageObj.attachments[0].url.replace('cdn.discordapp.com', 'media.discordapp.net')
                embed.add_field(name="Attachment", value=new_url)
    
    channel = discord.utils.get(deletedMessageObj.guild.channels, name="admin-logs")
    if channel != None:
        await channel.send("", embed=embed)
        
        
async def logEditedMessage(client, messageObjBeforeEdit, messageObjAfterEdit):
    if messageObjBeforeEdit.author == client.user:
        return
    
    embed = discord.Embed(title="Edited message event.")
    embed.add_field(name="User who edited the message:", value=(f'{messageObjBeforeEdit.author.name} | {messageObjBeforeEdit.author.display_name}'), inline=False)
    embed.add_field(name="The channel the message was sent in:", value=messageObjBeforeEdit.channel.name, inline=False)
    embed.add_field(name="What the message said before the edit:", value=messageObjBeforeEdit.content, inline=False)
    embed.add_field(name="What the message said after the edit:", value=messageObjAfterEdit.content, inline=False)
    
    embed.add_field(name="Image attached to message before edit:", value="", inline=False)
    
    
    if messageObjBeforeEdit.attachments:
        if len(messageObjBeforeEdit.attachments) == 1:
            if messageObjBeforeEdit.attachments[0].url.endswith(('.jpg', '.png', '.jpeg', '.gif')):
                new_url = messageObjBeforeEdit.attachments[0].url.replace('cdn.discordapp.com', 'media.discordapp.net')
                embed.set_image(url=new_url)
            else:
                new_url = messageObjBeforeEdit.attachments[0].url.replace('cdn.discordapp.com', 'media.discordapp.net')
                embed.add_field(name="Attachment", value=new_url)
    
    channel = discord.utils.get(messageObjBeforeEdit.guild.channels, name="admin-logs")
    if channel != None:
        await channel.send("", embed=embed)