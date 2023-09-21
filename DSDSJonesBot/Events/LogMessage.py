import discord

async def logMessage(client, messageObj):
    messageAuthor = messageObj.author.display_name
    messageContent = messageObj.content
    messageChannel = messageObj.channel.name
    
    with open("Resources/MessageLog.txt", "a") as file:
        file.write(f'{messageAuthor} in {messageChannel}: {messageContent}')
        file.write("\n")
    
    