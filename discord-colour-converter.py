#takes color in HEX
color = input("Please input a colour in HEX form, with the hastag ->  ")

#valid Hex chars
valid_char=["0","1","2","3",'4','5','6','7,','8','9','a','b','c','d','e','f','#']

#function to convert to discord color
def convert():
  lower_color = color.lower()
  discord_colour = lower_color.replace("#", "0x")
  print(discord_colour)
  
#checks if the characters in "color" are valid Hex characters
validation = [i in valid_char for i in color]
valid_hex = all(validation)

#makes sure the length of the color is proper hex, it begins with #, and the characters are valid characters
if len(color) == 7 and color[0] == "#" and valid_hex==True:
  convert()
#if the Hex color/form (idk the proper name) is invalid the program shuts off, lets the user know the HEX is invalid and tells them to run the script again
else:
  print("not valid HEX code, please try again")
  
