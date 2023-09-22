import discord
import asyncio
import time
from Commands import Verify, CreateReactRoles, Say, FindIncorrectNames
from Events import LogDeletedOrEditedMessages, LogChatInLeaderboard, LogMessage

#--disable the creation of pycache
import sys
sys.dont_write_bytecode = True
#---------------------------------



#--create the discord bot client with the proper intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.guild_typing = True
intents.guilds = True
intents.reactions = True
client = discord.Client(intents=intents, max_messages=3000)
#--------------------------------------------------------


#class for the function of the CQ buttons
class cqButtons(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    #function of attached to the "On shift" button
    @discord.ui.button(style=discord.ButtonStyle.danger, label="On shift", custom_id="ONSHIFTBUTTON")
    async def onShiftButton(self, interaction : discord.Interaction, button : discord.ui.Button):
        interactingUser = interaction.user
        cqRole = discord.utils.get(interaction.channel.guild.roles, name="CQ")
        await interactingUser.add_roles(cqRole)
        
        logChannel = discord.utils.get(interaction.guild.channels, name="cq-logs")
        if logChannel:
            logEmbed = discord.Embed(title=f"{interactingUser.display_name} has started a CQ shift.")
            await logChannel.send("", embed=logEmbed)
        
        await interaction.response.defer()
        
        #--------if the user hasn't ended their shift in 3900 seconds (65 minutes), remove the role.
        await asyncio.sleep(3900)
        
        #re-interate through members list to get an updated member obj with current roles
        for member in interaction.channel.guild.members:
            if member.name == interactingUser.name:
                if cqRole in member.roles:
                    
                    await member.remove_roles(cqRole)
                    
                    if logChannel:
                        logEmbed = discord.Embed(title=f"{member.display_name} has been on shift for more than 65 minutes, ending shift automatically.")
                        await logChannel.send("", embed=logEmbed)
            
        
    @discord.ui.button(style=discord.ButtonStyle.blurple, label="Off shift", custom_id="OFFSHIFTBUTTON")
    async def offShiftButton(self, interaction : discord.Interaction, button : discord.ui.Button):
        interactingUser = interaction.user
        cqRole = discord.utils.get(interaction.channel.guild.roles, name="CQ")
        if cqRole in interactingUser.roles:
            await interactingUser.remove_roles(cqRole)
        
            logChannel = discord.utils.get(interaction.guild.channels, name="cq-logs")
            if logChannel:
                logEmbed = discord.Embed(title=f"{interactingUser.display_name} has ended a CQ shift.")
                await logChannel.send("", embed=logEmbed)
        
        await interaction.response.defer()
#--------------------


@client.event
async def on_ready():
    print(f'DSDS Jones logged in as {client.user}')
    await client.change_presence(activity=discord.Game(name="with my campaign hat"))
    
    #make cq buttons work after bot restart
    client.add_view(cqButtons())

@client.event
async def on_message(messageObj):
    if messageObj.author == client.user:
        return
    
    await LogChatInLeaderboard.logMessageToLeaderboard(client, messageObj)
    await LogMessage.logMessage(client, messageObj)
    
    messageContent = messageObj.content.lower()
    
    match messageContent:
        case "m?create cq buttons":
            embed = discord.Embed(title="Charlie 369 CQ", colour=0xe1ff00)
            await messageObj.channel.send("", view=cqButtons(), embed = embed)
        
        case "verify":
            await Verify.verify(client, messageObj)
            
        case "m?create blank react roles":
            await CreateReactRoles.createReactionRoles(client, messageObj)
            
        case "m?create blank unique react roles":
            await CreateReactRoles.createReactionRoles(client, messageObj)
            
        case "m?say":
            await Say.say(client, messageObj)
            
        case "m?changestatus":
            await messageObj.reply("Type a status.")
            givenStatus = await client.wait_for("message", check=(lambda m: m.author == messageObj.author), timeout=60)
            await client.change_presence(activity=discord.Game(name=givenStatus.content))
            
        case "m?findincorrectnames":
            await FindIncorrectNames.findIncorrectNames(client, messageObj)
            
        case "chat leaderboard":
            await LogChatInLeaderboard.displayLeaderboard(client, messageObj)





#--------reaction roles
reactionRoleCoolDown = {}

@client.event
async def on_raw_reaction_add(payload):
    global reactionRoleCoolDown
    
    #if the reaction is added by the bot, ignore
    if payload.member == client.user:
        return
    
    
    
        
    fetchedGuild = client.get_guild(payload.guild_id)
    fetchedMember = await fetchedGuild.fetch_member(payload.user_id)
    fetchedChannel = client.get_channel(payload.channel_id)
    fetchedMessage = await fetchedChannel.fetch_message(payload.message_id)
    
    
    #--this just adds a little cooldown, because when you react a bunch of times quickly, it bugs out
    if payload.user_id in reactionRoleCoolDown.keys():
        if time.time() - reactionRoleCoolDown[payload.user_id] < 1:
            await fetchedMessage.remove_reaction(payload.emoji.name, fetchedMember)
            return
        else:
            del reactionRoleCoolDown[payload.user_id]
    
    reactionRoleCoolDown[payload.user_id] = time.time()
    
    #--check to see if the reacted message has embeds, filters out normal user sent messages
    if fetchedMessage.embeds != []:
        
        #--iterate through fields added to the embed, all different fields are different roles and emojis
        for field in fetchedMessage.embeds[0].fields:
            
            #--interpret the field, break it up into the emoji given, and the role
            #--fields made with "m?create blank react roles" are made as "1️⃣ - @E1 (PVT)" for example
            emojiInField = field.value.split(" - ")[0]
            if discord.PartialEmoji.from_str(emojiInField) == payload.emoji: #--check to see if emoji is valid
                
                givenRole = fetchedGuild.get_role(int(field.value.split(" - ")[1][3:-1]))#--get role from server, role id is interpreted from format like this "<@&1142512701269090354>"
                
                if fetchedMessage.embeds[0].description != None: #--when a unique react role is made, only one role can be taken at a time
                    if fetchedMessage.embeds[0].description.lower() == "unique": #--unique react roles are identified by this being in the desc
                        
                        #--for every role user has, compare it to the react role fields, if its a role that is not the one being requested, remove it and the reaction
                        for userRole in fetchedMember.roles: 
                            for recField in fetchedMessage.embeds[0].fields: 
                                if (userRole == fetchedGuild.get_role(int(recField.value.split(" - ")[1][3:-1])) and userRole != givenRole):
                                    await fetchedMember.add_roles(givenRole)
                                    await fetchedMember.remove_roles(userRole)
                                    await fetchedMessage.remove_reaction(recField.value.split(" - ")[0], fetchedMember)
                                    return
                
                #--if it was not a "unique" reaction role embed, just give them the role with no checks
                await fetchedMember.add_roles(givenRole)
                
                
        
@client.event
async def on_raw_reaction_remove(payload):
    fetchedGuild = client.get_guild(payload.guild_id)
    fetchedMember = await fetchedGuild.fetch_member(payload.user_id)
    fetchedChannel = client.get_channel(payload.channel_id)
    fetchedMessage = await fetchedChannel.fetch_message(payload.message_id)
    
    if fetchedMember == client.user:
        return
    
    #--remove role associated with removed reaction
    if fetchedMessage.embeds != []:
        for field in fetchedMessage.embeds[0].fields:
            emojiInField = field.value.split(" - ")[0]
            if discord.PartialEmoji.from_str(emojiInField) == payload.emoji:
                removedRole = fetchedGuild.get_role(int(field.value.split(" - ")[1][3:-1]))
                await fetchedMember.remove_roles(removedRole)
                return

    
@client.event
async def on_message_delete(deletedMessage):
    await LogDeletedOrEditedMessages.logDeletedMessage(client, deletedMessageObj=deletedMessage)
    
    
@client.event
async def on_message_edit(beforeEdit, afterEdit):
    await LogDeletedOrEditedMessages.logEditedMessage(client, beforeEdit, afterEdit)
    
        
            
#-------welcome messages            
@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.channels, name="✅┃verify")
    await channel.send("Welcome to the server! "+member.mention+' type "verify" to begin the verification process.')
    
    
    
            
        
        
