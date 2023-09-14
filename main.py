#libs
import discord
from discord import app_commands
from discord.ext import commands
import os
from discord.app_commands import CommandTree
import asyncio
import sqlite3

#client and command tree setup
intents = discord.Intents().all()
client = discord.Client(intents=intents)
tree = CommandTree(client)
client.tree = tree

logo_url = "url"

#sqlite setup
num_warnings = 0

conn = sqlite3.connect('warnings.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS warnings(
  user_id INTEGER PRIMARY KEY,
  num_warnings INTEGER)
''')
conn.commit()
conn.close()

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
        await user.add_roles(guild.get_role(PING_ROLE_ID)
        embed = discord.Embed(title="Role Given")
        embed.add_field(name="You were given the 'Bot Update Ping Role' in 'Mike's Server'", value="If you would not like this role please remove your reaction")
        embed.set_thumbnail(url=logo_url)
        await user.send(embed=embed)
    elif payload.message_id == int(PING_ROLE_ID) and emoji_str != emoji:
        pass
    elif payload.message_id == MSG_ID_2 and emoji_str == emoji:
        await user.add_roles(guild.get_role(POLL_ROLE)
        embed = discord.Embed(title="Role Given")
        embed.add_field(name="You were given the 'Poll Role' in 'Mike's Server'", value="If you would not like this role please remove your reaction")
        embed.set_thumbnail(url=logo_url)
        await user.send(embed=embed)
    elif payload.message_id == MSG_ID_2 and emoji_str != emoji:
        pass
    
#reaction roles remove
@client.event
async def on_raw_reaction_remove(payload):
    emoji = "👍"
    emoji_str = str(payload.emoji)
    guild = client.get_guild(payload.guild_id)
    user = guild.get_member(payload.user_id)
    message_id = MSG_ID
    message_id2 = MSG_ID_2
    role_id = PING_ROLE_ID
    role_id2 = POLL_ROLE
    if payload.message_id == message_id and emoji_str == emoji:
        await user.remove_roles(guild.get_role(role_id))
    elif payload.message_id == message_id and emoji_str != emoji:
        pass
    elif payload.message_id == message_id2 and emoji_str == emoji:
        await user.remove_roles(guild.get_role(role_id2))
    elif payload.message_id == message_id and emoji_str != emoji:
        pass

@client.event
async def on_member_join(user):
  verified_role = discord.utils.get(user.guild.roles,id = VERIFIED)
  joined_role = discord.utils.get(user.guild.roles, id = JOINED)
  await user.add_roles(joined_role)
  embed1 = discord.Embed(title = "Thank you for joining",)
  embed1.add_field(name = 'Please wait two minutes', value='After those two minutes you will be given the "verified" role')
  embed1.set_thumbnail(url = logo_url)
  await user.send(embed=embed1)
  await asyncio.sleep(120)
  await user.add_roles(verified_role)
  embed2 = discord.Embed(title="You have been verified. Enjoy our server!")
  embed2.set_thumbnail(url = logo_url)
  await user.send(embed=embed2)


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
    embed.set_thumbnail(url=logo_url)
    await interaction.response.send_message(embed=embed)
    request = f'{interaction.user.name} was banned for {ban_reason.name}. {interaction.user.name} wants to be unbanned because "{unban_reason}", {interaction.user.name} would also like to mention that "{additional_info}", '

    user1 = client.get_user(Id1)
    embed2 = discord.Embed(title="Ban appeal submitted", color = 0xffff00)
    embed2.add_field(name=f"Appeal submitted by {interaction.user.name}", value=request)
    embed2.set_thumbnail(url=logo_url)
    await user1.send(embed=embed2)
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
    embed.set_thumbnail(url=logo_url)
    embed2 = discord.Embed(title="HERE", color = 0x0000ff, url = "server")
    embed2.add_field(name="Submit Appeal Server", value="please submit your ban appeal here, nowhere else.")
    embed2.set_thumbnail(url=logo_url)
    await user.send(embed=embed)
    await user.send(embed=embed2)
    
    await interaction.guild.ban(user,reason=reason)
    embed3 = discord.Embed(title="User was banned", color = 0x9e578a,)
    embed3.add_field(name = "Banned", value=f'{user.mention} has been banned for "{reason}"')
    embed3.set_thumbnail(url=logo_url)
    await interaction.response.send_message(embed = embed3)
  except Exception as e:
    embed4= discord.Embed(title=f"Unable to ban {user}", color = 0x992d22)
    embed4.add_field(name="Ban failure",value=f"""An error occured when you tried to ban this user. You likely do not have the permissions to ban this member. 
    
    ERROR = {e}""")
    embed4.set_thumbnail(url=logo_url)
    await interaction.response.send_message(embed=embed4)

@client.tree.command(name="warn", description = "Warns a user")
@app_commands.describe(user="User you want to warn")
@app_commands.describe(reason="Reason for warning")
@commands.has_permissions(ban_members=True)
async def warn(interaction:discord.Interaction, user: discord.Member, reason:str):
  #sqlite 
  global num_warnings
  conn = sqlite3.connect('warnings.db')
  cursor = conn.cursor()
  cursor.execute("INSERT or REPLACE INTO warnings VALUES(?,?)",(user.id,num_warnings))
  cursor.execute(f"UPDATE warnings SET num_warnings = num_warnings + 1 WHERE user_id = {user.id}")
  num_warnings = cursor.execute("SELECT user_id, num_warnings FROM warnings").fetchall()
  num_warnings = num_warnings[0][1]
  conn.commit()
  conn.close()
  #actual stuff you see in discord
  embed=discord.Embed(title="You have been warned", color = 0xff0000)
  embed.add_field(name="Warned", value=f"You were warned by {interaction.user.name} for {reason}",)
  embed.set_thumbnail(url=logo_url)
  await user.send(embed=embed)
  embed2 = discord.Embed(title="User warned", color = 0x992d22)
  embed2.add_field(name=f"{user}",value="")
  await interaction.response.send_message(embed=embed2)

@client.tree.command(name="get_warns",description = "get the number of warnings and reason for warns of a user")
@commands.has_permissions(ban_members=True)
async def get_warns(interaction:discord.Interaction, user: discord.Member):
  conn = sqlite3.connect('warnings.db')
  cursor = conn.cursor()
  warn_info = cursor.execute(f"SELECT num_warnings FROM warnings WHERE user_id = {user.id}").fetchall()
  warn_info = warn_info[0][0]
  conn.commit()
  conn.close()
  embed = discord.Embed(title=f"Warning info for {user.name}",color=0xff0000)
  embed.add_field(name=f"{user.name} has {warn_info} warnings",value="you may remove a warning with /remove_warn (not actually a command yet)")
  embed.set_thumbnail(url=logo_url)
  await interaction.response.send_message(embed=embed)
  
#deny appeal command
@client.tree.command(name="deny", description = "Denies a ban appeal")
@app_commands.describe(user="The user you want to deny from being unbanned")
@app_commands.describe(reason="Reason for denial")
@commands.has_permissions(ban_members=True)
async def deny(interaction:discord.Interaction, user: discord.Member, reason:str):
  embed=discord.Embed(title="Appeal Denied", color = 0xff0000)
  embed.add_field(name="Denied", value=f"Your ban appeal was denied for {reason}")
  embed.set_thumbnail(url=logo_url)
  await user.send(embed=embed)

#accept appeal command
@client.tree.command(name="accept", description = "Accepts a ban appeal")
@app_commands.describe(user="The user you want to accept appeal for")
@commands.has_permissions(ban_members=True)
async def accept(interaction:discord.Interaction, user: discord.Member):
  embed=discord.Embed(title="Appeal Accepted", color = 0xff0000)
  embed.add_field(name="Accepted", value="Your ban appeal 'Mike's Server' was accept, you will be unbanned shortly")
  embed.set_thumbnail(url=logo_url)
  await user.send(embed=embed)

#help command
@client.tree.command(name="help", description = "Takes you to the bot's GitHub wiki")
async def help(interaction=discord.Interaction):
  embed = discord.Embed(title="Github Wiki", color = 0xffff00, url="https://github.com/Simply-Cubing/Mikes-Server-Discord-Bot/wiki")
  embed.add_field(name="Wiki", value ="Open the Github wiki to find a command list for this bot")
  embed.set_thumbnail(url=logo_url)
  await interaction.response.send_message(embed=embed)

#allows moderators/admins to send embeds for annouements, etc
@client.tree.command(name="send_embed", description = "Let's admins send annoucements and messages as embeds, for aesthetic")
@app_commands.describe(inline = 'Select whether or not you want the embed to have the "inline" formatting')
@commands.has_permissions(ban_members=True)
async def send_embed(interaction: discord.Interaction, inline: bool, title: str, name:str, value:str, color:int):
  embed= discord.Embed(title=title,color=color)
  embed.add_field(name=name, value = value, inline = inline)
  embed.set_thumbnail(url=logo_url)
  await interaction.response.send_message(embed=embed)

#button class
class Buttons(discord.ui.View):
    def __init__(self, *, timeout=180):
        super().__init__(timeout=timeout)
    @discord.ui.button(label="Suggestion Ticket",style=discord.ButtonStyle.green)
    #functions for different buttons
    async def suggest_button(self,interaction:discord.Interaction,button:discord.ui.Button):
      channel = client.get_channel(int(os.environ['SUGGESTION_CHANNEL_ID']))
      guild = interaction.guild
      user = interaction.user
      await interaction.user.add_roles((guild.get_role(int(os.environ['SUGGESTION_ROLE_ID']))))
      embed=discord.Embed(title="You have opened ticketing room with the admins",color=0xff0000)
      embed.add_field(name="Please remain patient as you wait for an admin to get online",value="Thank You")
      embed.set_thumbnail(url=logo_url)
      await user.send(embed=embed)
      await channel.send(f"{user.mention} you may discuss your issue with the admins here")
      await interaction.response.send_message(embed=embed,ephemeral = True)
    @discord.ui.button(label="Report Ticket",style=discord.ButtonStyle.blurple) 
    async def report_ticket(self,interaction:discord.Interaction,button:discord.ui.Button):
      channel = client.get_channel(int(os.environ['REPORT_CHANNEL_ID']))
      guild = interaction.guild
      user = interaction.user
      await interaction.user.add_roles((guild.get_role(int(os.environ['REPORT_ROLE_ID']))))
      embed=discord.Embed(title="You have opened ticketing room with the admins",color=0xff0000)
      embed.add_field(name="Please remain patient as you wait for an admin to get online",value="Thank You")
      embed.set_thumbnail(url=logo_url)
      await user.send(embed=embed)
      await channel.send(f"{user.mention} you may discuss your issue with the admins here")
      await interaction.response.send_message(embed=embed,ephemeral = True)
    @discord.ui.button(label="Miscellaneous Ticket",style=discord.ButtonStyle.red,) 
    async def miscellaneous_button(self,interaction:discord.Interaction,button:discord.ui.Button):
      channel = client.get_channel(int(os.environ['MISC_CHANNEL_ID']))
      guild = interaction.guild
      user = interaction.user
      await interaction.user.add_roles((guild.get_role(int(os.environ['MISC_ROLE_ID']))))
      embed=discord.Embed(title="You have opened ticketing room with the admins",color=0xff0000)
      embed.add_field(name="Please remain patient as you wait for an admin to get online",value="Thank You")
      embed.set_thumbnail(url=logo_url)
      await user.send(embed=embed)
      await channel.send(f"{user.mention} you may discuss your issue with the admins here")
      await interaction.response.send_message(embed=embed,ephemeral = True)

@client.tree.command(name="ticket",description="Submit a ticket so you can discuss issues with the admins")
async def ticket(interaction:discord.Interaction):
  await interaction.response.send_message("What kind of ticket do you want to submit",view=Buttons())

@client.tree.command(name="purge",description="deletes all messages")
@app_commands.checks.has_permissions(ban_members=True)
async def purge(interaction:discord.Interaction,limit:int):
  await interaction.response.send_message("Purging")
  await interaction.channel.purge(limit=limit)

@client.tree.command(name="get_math_question",description="get a math question")
async def math(interaction:discord.Interaction):
  num1 = random.randint(1,20)
  num2 = random.randint(1,20)
  global num_answer
  num_answer = num1+num2
  embed = discord.Embed(title=f"""Q: {num1} + {num2}


run /submit_answer to type your answer""",color = 0xabcdef)
  embed.set_thumbnail(url=logo_url)
  await interaction.response.send_message(embed=embed)
  
  global starttime
  starttime = time.time()
  
@client.tree.command(name="submit_answer",description="submit your answer to the question")
@app_commands.describe(answer="your answer to the math question")
async def submit_answer(interaction:discord.Interaction,answer:int):
  global num_answer
  global starttime
  if answer == num_answer:
    answer_time = round((time.time() - starttime),3)
    embed= discord.Embed(title=f"Correct! it took you {answer_time} seconds to solve the problem")
    embed.set_image(url="https://streamsentials.com/wp-content/uploads/pogchamp-twitch-emote.png")
    embed.set_thumbnail(url=logo_url)
    await interaction.response.send_message(embed=embed)
  else:
    embed=discord.Embed(title=f"Incorrect, the answer was {num_answer}")
    embed.set_image(url="https://www.pngkey.com/png/detail/14-142665_pepe-png.png")
    embed.set_thumbnail(url=logo_url)
    await interaction.response.send_message(embed=embed)

client.run(TOKEN)
