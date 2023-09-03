import discord




async def verify(client, messageObj):

#----verification
    if messageObj.channel.name[-6:] == "verify":
    #-------------------------------------------------verification---------------------------------------------------------------------------#
        ckRole = discord.utils.get(messageObj.channel.guild.roles, name="Crimson Knight")
        
        if ckRole in messageObj.author.roles:
            await messageObj.reply("You're already verified.")
            await messageObj.channel.send(file=discord.File("Resources\VerifiedImage.png"))
        #-------------------------------------------------------------------------------------------------------------------
        else:
            await messageObj.reply("Please send your first name")
            repliedMsg1 = await client.wait_for("message", check=(lambda m: m.author == messageObj.author))
            
            
            await repliedMsg1.reply("Please send your last name")
            repliedMsg2 = await client.wait_for("message", check=(lambda m: m.author == messageObj.author))
            
            reactionConfirmation = await repliedMsg2.reply(f'Is this your name?: {repliedMsg2.content}, {repliedMsg1.content}')
            await reactionConfirmation.add_reaction("👍")
            await reactionConfirmation.add_reaction("👎")
            
            global agreed
            agreed = False
            
            def check(reaction, user):
                global agreed
                if str(reaction.emoji) == "👍":
                    agreed = True
                return user == messageObj.author
            

            await client.wait_for("reaction_add", check=check, timeout=120)
            if agreed == True:
                await messageObj.author.add_roles(ckRole)
                try:
                    await messageObj.author.edit(nick=f'{repliedMsg2.content}, {repliedMsg1.content}')
                except:
                    await messageObj.reply("Missing nickname permissions.")
                    
                await messageObj.channel.send(file=discord.File("Resources\VerifiedImage.png"))
            else:
                await messageObj.reply("Reuse the m?verify command to start over.")
                
        return
    