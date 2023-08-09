import discord
from discord import app_commands
from discord.ext import commands
import os

intents = discord.Intents().all()
#yes i use all() don't ask
client = commands.Bot(command_prefix='!', intents=intents)

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


#submit appeal command

@client.tree.command(name="submit_appeal")
@app_commands.describe(ban_reason="cause of your ban, if you choose 'other' please fill out the 'additional_info' parameter ")
@app_commands.describe(unban_reason="why should you be unbanned")
@app_commands.describe(ban_reason='unban reasons')
#choices for reasons of ban
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
@app_commands.describe(additional_info="add extra comments OR if you chose 'other' as your ban reason put it here")
async def add(interaction: discord.Interaction, ban_reason: discord.app_commands.Choice[int], unban_reason: str, additional_info:str=None):
  
  await interaction.response.send_message("Your ban appeal has been sent and is now pending.")
  request = f'{interaction.user.name} was banned for {ban_reason.name}, {interaction.user.name} wants to be unbanned because "{unban_reason}", {interaction.user.name} would also like to mention that "{additional_info}", '
    
  user1 = client.get_user(id1)
  user2 = client.get_user(id2)
  await user1.send(request)
  await user2.send(request)
#bans user
@client.tree.command(name="ban")
@app_commands.describe(reason = "reason for ban")
@app_commands.describe(user="the user you want to ban")
@commands.has_permissions(ban_members=True)
async def ban(interaction:discord.Interaction, user:discord.Member, reason:str):
  #bans user and dms the user that they were banned
  try:
    await user.send(f"You have been banned from 'Mike's Server' for {reason} if you would like to submit an appeal to be unbanned please use '/submit_appeal'")
    await interaction.guild.ban(user,reason=reason)
    await interaction.response.send_message(f'User {user.mention} has been banned for "{reason}"')
  #lets the user know that they're unable to ban a user instead of returning an error
  except:
    await interaction.response.send_message("You do not have the permissions to ban this member")
  
  
client.run(TOKEN)
