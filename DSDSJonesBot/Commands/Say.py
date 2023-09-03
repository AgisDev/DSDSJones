import discord


async def say(client, messageObj):
    await messageObj.reply("What channel is desired?")
    
    channelName = await client.wait_for("message", check=(lambda m: m.author == messageObj.author), timeout=60)
    
    await messageObj.reply("What needs to be said?")
    
    givenMessage = await client.wait_for("message", check=(lambda m: m.author == messageObj.author), timeout=60)
    
    channel = discord.utils.get(messageObj.channel.guild.channels, name=channelName.content)
    
    for channel in messageObj.channel.guild.channels:
        if channel.name == channelName.content or channel.name[-(len(channelName.content)):] == channelName.content:
            await channel.send(givenMessage.content)