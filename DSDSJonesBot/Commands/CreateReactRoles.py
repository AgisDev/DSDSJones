import discord

async def createReactionRoles(client, messageObj):
    messageContent = messageObj.content
    
    
    
    await messageObj.reply("Define a title for the react roles")
    embedTitle = await client.wait_for("message", check=(lambda m: m.author == messageObj.author), timeout=60)
    
    if messageContent.lower() == "m?create blank react roles":
        msgEmbed = discord.Embed(title=embedTitle.content)
    else:
        msgEmbed = discord.Embed(title=embedTitle.content, description="Unique")
    
    global reactRoleMessage
    reactRoleMessage = await messageObj.channel.send(embed=msgEmbed)
    
    async def requestInfoForField():
        
        global reactRoleMessage
        
        askEmojiMessage = await messageObj.channel.send("Send a valid emoji for the first reaction role, or type cancel to cancel",)
        
        repliedEmoji = await client.wait_for("message", check=(lambda m: m.author == messageObj.author), timeout=60)
        
        
        if repliedEmoji.content.lower() == "cancel":
            await askEmojiMessage.delete()
            await repliedEmoji.delete()
            return
        
        if len(repliedEmoji.content) > 4:
            await askEmojiMessage.delete()
            await repliedEmoji.delete()
            await requestInfoForField()
            return
        
        await askEmojiMessage.delete()
        await repliedEmoji.delete()
        
        askRoleMessage = await messageObj.channel.send("Send a valid role name for the first reaction role, or type cancel to cancel")
        repliedRole = await client.wait_for("message", check=(lambda m: m.author == messageObj.author), timeout=60)
        
        if repliedRole.content.lower() == "cancel":
            await askRoleMessage.delete()
            await repliedRole.delete()
            return
        
        guildRole = discord.utils.get(messageObj.channel.guild.roles, name=repliedRole.content)
        
        if guildRole == None:
            await askRoleMessage.delete()
            await repliedRole.delete()
            await requestInfoForField()
            return
        
        await askRoleMessage.delete()
        await repliedRole.delete()
        
        fieldInfo = repliedEmoji.content+" - "+guildRole.mention
        
        pastEmbed = reactRoleMessage.embeds[0]
        pastEmbed.add_field(name="", value=fieldInfo, inline=False)
        
        await reactRoleMessage.edit(embed = pastEmbed)
        
        await messageObj.channel.send("Reaction role added.", delete_after=5)
        
        try:
            await reactRoleMessage.add_reaction(repliedEmoji.content)
        except:
            print("Invalid emoji given.")
            
        await requestInfoForField()
    
    await requestInfoForField()