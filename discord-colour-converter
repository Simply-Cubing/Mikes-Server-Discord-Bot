#takes colour in hex
color = input("Please input a colour in HEX form, with the hastag ->  ")
#function which converts the HEX colour to discord's colour form 
def convert():
  lower_color = color.lower()
  discord_colour = lower_color.replace("#", "0x")
  print(discord_colour)
#makes sure its written properly
if len(color) == 7 and color[0] == "#":
  convert()
#lets the user no that their colour is invalid
else:
  print("not valid HEX code, please try again")
