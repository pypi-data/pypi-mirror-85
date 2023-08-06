import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
import json

client = commands.Bot(command_prefix=".")


#arg1 = ""
#arg2 = ""
#arg3 = ""
#arg4 = ""
#arg5 = ""
#arg6 = ""
#arg7 = ""
#arg8 = ""
#arg9 = ""
#arg10 = ""

#bot_message = ""


command_list = []

command_dict = {}

arg_number = 0

class simple_discord_bot(discord.Client):
    def __init__(self, token):
        self.bot_token = token
    def add_command(self, command_to_add, response, react_to=None, reaction=None, delete=False, connect_to_voicechannel=False, source_to_play=None, DM=False):

        command_dict[str(command_to_add)] = {
        "response" : response,
        "react_to" : react_to,
        "reaction" : reaction,
        "delete" : delete,
        "connect_to_voicechannel" : connect_to_voicechannel,
        "source_to_play" : source_to_play,
        "DM" : DM
        }

        command_list.append(command_to_add)


@client.event
async def on_ready():
    print(f"Successfully logged in to Discord as user '{client.user}'")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    for c in command_list:
        if str(message.content).startswith(c):

#            message_content_list_seperated_by_spaces = f"{message.content}".split(" ")
#            argument_count = len(message_content_list_seperated_by_spaces)
#
#            global arg1
#            global arg2
#            global arg3
#            global arg4
#            global arg5
#            global arg6
#            global arg7
#            global arg8
#            global arg9
#            global arg10
#
#            if argument_count == 1:
#                arg1 = message_content_list_seperated_by_spaces[0]

#            if argument_count == 2:
#                arg1 = message_content_list_seperated_by_spaces[0]
#                arg2 = message_content_list_seperated_by_spaces[1]
#
#            if argument_count == 3:
#                arg1 = message_content_list_seperated_by_spaces[0]
#                arg2 = message_content_list_seperated_by_spaces[1]
#                arg3 = message_content_list_seperated_by_spaces[2]

#            if argument_count == 4:
#                arg1 = message_content_list_seperated_by_spaces[0]
#                arg2 = message_content_list_seperated_by_spaces[1]
#                arg3 = message_content_list_seperated_by_spaces[2]
#                arg4 = message_content_list_seperated_by_spaces[3]
#
#            if argument_count == 5:
#                arg1 = message_content_list_seperated_by_spaces[0]
#                arg2 = message_content_list_seperated_by_spaces[1]
#                arg3 = message_content_list_seperated_by_spaces[2]
#                arg4 = message_content_list_seperated_by_spaces[3]
#                arg5 = message_content_list_seperated_by_spaces[4]

#            if argument_count == 6:
#                arg1 = message_content_list_seperated_by_spaces[0]
#                arg2 = message_content_list_seperated_by_spaces[1]
#                arg3 = message_content_list_seperated_by_spaces[2]
#                arg4 = message_content_list_seperated_by_spaces[3]
#                arg5 = message_content_list_seperated_by_spaces[4]
#                arg6 = message_content_list_seperated_by_spaces[5]

#            if argument_count == 7:
#                arg1 = message_content_list_seperated_by_spaces[0]
#                arg2 = message_content_list_seperated_by_spaces[1]
#                arg3 = message_content_list_seperated_by_spaces[2]
#                arg4 = message_content_list_seperated_by_spaces[3]
#                arg5 = message_content_list_seperated_by_spaces[4]
#                arg6 = message_content_list_seperated_by_spaces[5]
#                arg7 = message_content_list_seperated_by_spaces[6]
#
#            if argument_count == 8:
#                arg1 = message_content_list_seperated_by_spaces[0]
#                arg2 = message_content_list_seperated_by_spaces[1]
#                arg3 = message_content_list_seperated_by_spaces[2]
#                arg4 = message_content_list_seperated_by_spaces[3]
#                arg5 = message_content_list_seperated_by_spaces[4]
#                arg6 = message_content_list_seperated_by_spaces[5]
#                arg7 = message_content_list_seperated_by_spaces[6]
#                arg8 = message_content_list_seperated_by_spaces[7]

#            if argument_count == 9:
#                arg1 = message_content_list_seperated_by_spaces[0]
#                arg2 = message_content_list_seperated_by_spaces[1]
#                arg3 = message_content_list_seperated_by_spaces[2]
#                arg4 = message_content_list_seperated_by_spaces[3]
#                arg5 = message_content_list_seperated_by_spaces[4]
#                arg6 = message_content_list_seperated_by_spaces[5]
#                arg7 = message_content_list_seperated_by_spaces[6]
#                arg8 = message_content_list_seperated_by_spaces[7]
#                arg9 = message_content_list_seperated_by_spaces[8]



#            if argument_count == 10:
#                arg1 = message_content_list_seperated_by_spaces[0]
#                arg2 = message_content_list_seperated_by_spaces[1]
#                arg3 = message_content_list_seperated_by_spaces[2]
#                arg4 = message_content_list_seperated_by_spaces[3]
#                arg5 = message_content_list_seperated_by_spaces[4]
#                arg6 = message_content_list_seperated_by_spaces[5]
#                arg7 = message_content_list_seperated_by_spaces[6]
#                arg8 = message_content_list_seperated_by_spaces[7]
#                arg9 = message_content_list_seperated_by_spaces[8]
#                arg10 = message_content_list_seperated_by_spaces[9]





#            command_dict[c]["arguments"] = {
#            "argument1" : arg1,
#            "argument2" : arg2,
#            "argument3" : arg3,
#            "argument4" : arg4,
#            "argument5" : arg5,
#            "argument6" : arg6,
#            "argument7" : arg7,
#            "argument8" : arg8,
#            "argument9" : arg9,
#            "argument10": arg10
#            }
#
#            arg1 = command_dict[c]["arguments"]["argument1"]
#            arg2 = command_dict[c]["arguments"]["argument2"]
#            arg3 = command_dict[c]["arguments"]["argument3"]
#            arg4 = command_dict[c]["arguments"]["argument4"]
#            arg5 = command_dict[c]["arguments"]["argument5"]
#            arg6 = command_dict[c]["arguments"]["argument6"]
#            arg7 = command_dict[c]["arguments"]["argument7"]
#            arg8 = command_dict[c]["arguments"]["argument8"]
#            arg9 = command_dict[c]["arguments"]["argument9"]
#            arg10 = command_dict[c]["arguments"]["argument10"]

#            if isinstance(command_dict[c]["response"], str):
            bot_message = await message.channel.send(command_dict[c]["response"])
#            if not isinstance(command_dict[c]["response"], str):
#                await message.channel.send(c["arguments"][response])
            if command_dict[c]["react_to"] != None:
                if command_dict[c]["react_to"] == "command":
                    await message.add_reaction(f"{command_dict[c]['reaction']}")

                if command_dict[c]["react_to"] == "response":
                    await bot_message.add_reaction(f"{command_dict[c]['reaction']}")

                if command_dict[c]["delete"] == True:
                    await message.delete()

            if command_dict[c]["connect_to_voicechannel"] != False:
                try:
                    channel_to_connnect_to = message.author.voice.channel
                    voice_object = await channel_to_connnect_to.connect()
                    if command_dict[c]["source_to_play"] == None:
                        print("Bot will not play audio because no source file was given.")
                        return
                    file_to_play = FFmpegPCMAudio(command_dict[c]["source_to_play"])
                    voice_object.play(file_to_play)
                    print(f"Playing audio from file '{command_dict[c]['source_to_play']}' in channel '{channel_to_connnect_to}'")

                except Exception as play_error:
                    if "already" in str(play_error):
                        print("Could not connect to voice channel because bot is already in it. Please disconnect before trying to connect again.")

                    if str(play_error) == "'NoneType' object has no attribute 'channel'":
                        print("Bot could not join voice channel because member is not in one.")

                    else:
                        print(str(play_error))
                    return

            if command_dict[c]["DM"] != False:
                try:
                    await message.author.send(str(command_dict[c]["DM"]))

                except Exception as DM_error:
                    print(str(DM_error))

try:
    print("Attempting to login to Discord...")
    client.run(simple_discord_bot.bot_token)
except Exception as login_error:
    print(login_error)
