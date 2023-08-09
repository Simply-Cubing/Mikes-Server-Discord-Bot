import discord
from discord import app_commands
from discord.ext import commands
import os


intents = discord.Intents().all()
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




@client.tree.command(name="submit_appeal")
@app_commands.describe(ban_reason="cause of your ban, if you choose 'other' please fill out the 'additional_info' parameter ")
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
@app_commands.describe(additional_info="add extra comments OR if you chose 'other' as your ban reason put it here")
async def add(interaction: discord.Interaction, ban_reason: discord.app_commands.Choice[int], unban_reason: str, additional_info:str=None):

  embed = discord.Embed(title="Appeal Sent", color = 0x992d22)
  embed.add_field(name="Thank you for submitting", value="Your appeal is now pending, the admins will get back to you shortly")
  await interaction.response.send_message(embed=embed)
  request = f'{interaction.user.name} was banned for {ban_reason.name}, {interaction.user.name} wants to be unbanned because "{unban_reason}", {interaction.user.name} would also like to mention that "{additional_info}", '

  user1 = client.get_user(Id1)
  user2 = client.get_user(Id2)
  embed2 = discord.Embed(title="Ban appeal submitted", color = 0xffff00)
  embed2.add_field(name=f"Appeal submitted by {interaction.user.name}", value=request)
  await user1.send(embed=embed2)
  await user2.send(embed=embed2)

@client.tree.command(name="ban")
@app_commands.describe(reason = "reason for ban")
@app_commands.describe(user="the user you want to ban")
@commands.has_permissions(ban_members=True)
async def ban(interaction:discord.Interaction, user:discord.Member, reason:str):
  try:
    embed = discord.Embed(title="You have been banned", color=0)
    embed.add_field(name = "Banned", value=f"You were banned for {reason}, if you would like to submit an appeal to be unbanned please join the server below and run '/submit_appeal'",)
    embed2 = discord.Embed(title="HERE", color = 0x0000FF, url = "link")
    embed2.add_field(name="Submit Appeal Server", value="please submit your ban appeal here, nowhere else.")
    await user.send(embed=embed)
    await user.send(embed=embed2)
    
    await interaction.guild.ban(user,reason=reason)
    embed3 = discord.Embed(title="User was banned", color = 0x9e578a,)
    embed3.add_field(name = "Banned", value=f'{user.mention} has been banned for "{reason}"')
    await interaction.response.send_message(embed = embed3)
  except Exception as e:
    embed4= discord.Embed(title=f"Unable to ban {user}", color = 0x992d22)
    embed4.add_field(name="Ban failure",value=f"""An error occured when you tried to ban this user, you likely do not have the permissions to ban this member. 
    
    ERROR = {e}""")
    await interaction.response.send_message(embed=embed4)
    
client.run(token)
