#libs
import discord
from discord import app_commands
from discord.ext import commands
import os
from keep_alive import keep_alive
from discord.app_commands import CommandTree

#client and command tree setup
intents = discord.Intents().all()
client = discord.Client(intents=intents)
tree = CommandTree(client)
client.tree = tree

#login messages
@client.event
async def on_ready():
  print('bot logged in!')
  print('--------------')
  print("connected to:")
  for guild in client.guilds:
    print("\t\t- {}".format(guild.name))
  await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="ban appeals"))
  print(f'''
> logged in as {client.user}''')
  try:
    synced = await client.tree.sync()
    print(f"Synced {len(synced)} command(s)")
  except Exception as e:
    print(f'Error syncing commands: {e}')

#reaction roles add
@client.event
async def on_raw_reaction_add(payload):
    emoji = "👍"
    emoji_str = str(payload.emoji)
    guild = client.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    if payload.message_id == MSG_ID and emoji_str == emoji:
        await user.add_roles(guild.get_role(bot_ping_role_id))
    elif payload.message_id == MSG_ID and emoji_str != emoji:
        pass
    elif payload.message_id == MSG_ID2 and emoji_str == emoji:
        await user.add_roles(guild.get_role(POLL_ROLE))
    elif payload.message_id == MSG_ID2 and emoji_str != emoji:
        pass
    
#reaction roles remove
@client.event
async def on_raw_reaction_remove(payload):
    emoji = "👍"
    emoji_str = str(payload.emoji)
    guild = client.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    message_id = int(os.environ['MSG_ID'])
    message_id2 = int(os.environ['MSG_ID_2'])
    role_id = int(os.environ['PING_ROLE_ID'])
    role_id2 = int(os.environ['POLL_ROLE'])
    if payload.message_id == message_id and emoji_str == emoji:
        await user.remove_roles(guild.get_role(role_id))
    elif payload.message_id == message_id and emoji_str != emoji:
        pass
    elif payload.message_id == message_id2 and emoji_str == emoji:
        await user.remove_roles(guild.get_role(role_id2))
    elif payload.message_id == message_id and emoji_str != emoji:
        pass

#submit appeal command
@client.tree.command(name="submit_appeal", description = "If you were banned and would like to be unbanned use submit a ban appeal here")
@app_commands.describe(ban_reason="cause of your ban, if you choose 'other' PLEASE fill out 'additional_info'")
@app_commands.describe(unban_reason="why should you be unbanned")
@app_commands.describe(ban_reason='unban reasons')
@app_commands.choices(ban_reason=[
  discord.app_commands.Choice(name='NSFW', value = 1),
  discord.app_commands.Choice(name='Discrimination', value = 2),
  discord.app_commands.Choice(name='Swearing/Vulgar language', value = 3),
  discord.app_commands.Choice(name='@everyone', value = 4),
  discord.app_commands.Choice(name='Using inappropriate channel', value = 5),
  discord.app_commands.Choice(name='Bullying', value = 6),
  discord.app_commands.Choice(name='Malicious files/links', value = 7),
  discord.app_commands.Choice(name='Misbehaving in voice chat', value = 8),
  discord.app_commands.Choice(name='Discussing controversial topics', value = 9),
  discord.app_commands.Choice(name='Disrespecting Privacy (asking for personal info)', value = 10),
  discord.app_commands.Choice(name='Spam', value = 11),
  discord.app_commands.Choice(name='Other', value = 12),
])
@app_commands.describe(additional_info="add extra comments, if you chose 'other' as your ban reason put it here")
async def add(interaction: discord.Interaction, ban_reason: discord.app_commands.Choice[int], unban_reason: str, additional_info:str=None):
  try:
    embed = discord.Embed(title="Appeal Sent", color = 0x992d22)
    embed.add_field(name="Thank you for submitting", value="Your appeal is now pending, the admins will get back to you shortly")
    embed.set_thumbnail(url="https://ih1.redbubble.net/image.3530640854.1334/st,small,507x507-pad,600x600,f8f8f8.u1.jpg")
    await interaction.response.send_message(embed=embed)
    request = f'{interaction.user.name} was banned for {ban_reason.name}. {interaction.user.name} wants to be unbanned because "{unban_reason}", {interaction.user.name} would also like to mention that "{additional_info}", '

    user1 = client.get_user(Id1)
    user2 = client.get_user(Id2)
    embed2 = discord.Embed(title="Ban appeal submitted", color = 0xffff00)
    embed2.add_field(name=f"Appeal submitted by {interaction.user.name}", value=request)
    embed2.set_thumbnail(url="https://ih1.redbubble.net/image.3530640854.1334/st,small,507x507-pad,600x600,f8f8f8.u1.jpg")
    await user1.send(embed=embed2)
    await user2.send(embed=embed2)
  except Exception as e:
    await interaction.response.send_message(e)


#ban command
@client.tree.command(name="ban", description ="Bans a user")
@app_commands.describe(reason = "reason for ban")
@app_commands.describe(user="the user you want to ban")
@commands.has_permissions(ban_members=True)
async def ban(interaction:discord.Interaction, user:discord.Member, reason:str):
  try:
    embed = discord.Embed(title="You have been banned", color=0)
    embed.add_field(name = "Banned", value=f"You were banned for {reason}. If you would like to submit an appeal to be unbanned please join the server below and run '/submit_appeal'",)
    embed.set_thumbnail(url="https://ih1.redbubble.net/image.3530640854.1334/st,small,507x507-pad,600x600,f8f8f8.u1.jpg")
    embed2 = discord.Embed(title="HERE", color = 0x0000ff, url = "https://discord.gg/Jnt3A5cS")
    embed2.add_field(name="Submit Appeal Server", value="please submit your ban appeal here, nowhere else.")
    embed2.set_thumbnail(url="https://ih1.redbubble.net/image.3530640854.1334/st,small,507x507-pad,600x600,f8f8f8.u1.jpg")
    await user.send(embed=embed)
    await user.send(embed=embed2)
    
    await interaction.guild.ban(user,reason=reason)
    embed3 = discord.Embed(title="User was banned", color = 0x9e578a,)
    embed3.add_field(name = "Banned", value=f'{user.mention} has been banned for "{reason}"')
    embed3.set_thumbnail(url="https://ih1.redbubble.net/image.3530640854.1334/st,small,507x507-pad,600x600,f8f8f8.u1.jpg")
    await interaction.response.send_message(embed = embed3)
  except Exception as e:
    embed4= discord.Embed(title=f"Unable to ban {user}", color = 0x992d22)
    embed4.add_field(name="Ban failure",value=f"""An error occured when you tried to ban this user. You likely do not have the permissions to ban this member. 
    
    ERROR = {e}""")
    embed4.set_thumbnail(url="https://ih1.redbubble.net/image.3530640854.1334/st,small,507x507-pad,600x600,f8f8f8.u1.jpg")
    await interaction.response.send_message(embed=embed4)

@client.tree.command(name="warn", description = "Warns a user")
@app_commands.describe(user="User you want to warn")
@app_commands.describe(reason="Reason for warning")
@commands.has_permissions(ban_members=True)
async def warn(interaction:discord.Interaction, user: discord.Member, reason:str):
  embed=discord.Embed(title="You have been warned", color = 0xff0000)
  embed.add_field(name="Warned", value=f"You were warned by {interaction.user.name} for {reason}",)
  embed.set_thumbnail(url="https://ih1.redbubble.net/image.3530640854.1334/st,small,507x507-pad,600x600,f8f8f8.u1.jpg")
  await user.send(embed=embed)
  embed2 = discord.Embed(title="User warned", color = 0x992d22)
  embed2.add_field(name=f"{user}",value="")
  await interaction.response.send_message(embed=embed2)
  
#deny appeal command
@client.tree.command(name="deny", description = "Denies a ban appeal")
@app_commands.describe(user="The user you want to deny from being unbanned")
@app_commands.describe(reason="Reason for denial")
@commands.has_permissions(ban_members=True)
async def deny(interaction:discord.Interaction, user: discord.Member, reason:str):
  embed=discord.Embed(title="Appeal Denied", color = 0xff0000)
  embed.add_field(name="Denied", value=f"Your ban appeal was denied for {reason}")
  embed.set_thumbnail(url="https://ih1.redbubble.net/image.3530640854.1334/st,small,507x507-pad,600x600,f8f8f8.u1.jpg")
  await user.send(embed=embed)

#accept appeal command
@client.tree.command(name="accept", description = "Accepts a ban appeal")
@app_commands.describe(user="The user you want to accept appeal for")
@commands.has_permissions(ban_members=True)
async def accept(interaction:discord.Interaction, user: discord.Member):
  embed=discord.Embed(title="Appeal Accepted", color = 0xff0000)
  embed.add_field(name="Accepted", value="Your ban appeal 'Mike's Server' was accept, you will be unbanned shortly")
  embed.set_thumbnail(url="https://ih1.redbubble.net/image.3530640854.1334/st,small,507x507-pad,600x600,f8f8f8.u1.jpg")
  await user.send(embed=embed)

#help command
@client.tree.command(name="help", description = "Takes you to the bot's github wiki")
async def help(interaction=discord.Interaction):
  embed = discord.Embed(title="Github Wiki", color = 0xffff00, url="https://github.com/Simply-Cubing/Mikes-Server-Discord-Bot/wiki")
  embed.add_field(name="Wiki", value ="Open the Github wiki to find a command list for this bot")
  await interaction.response.send_message(embed=embed)


keep_alive()
client.run(TOKEN)
