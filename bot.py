import discord
import random
import sound_names
import asyncio
import race_main


has_joined = False
is_ben = False
voice_client: discord.VoiceClient


FFMPEG_PATH = ""


async def play_sound(voice_channel: discord.VoiceChannel, sound_name: str):
    global has_joined, voice_client
    if not has_joined:
        voice_client = await voice_channel.connect()
        voice_client.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=sound_names.SOUNDS_NAMES_FILE + "/" + "прив.mp4"))
        while voice_client.is_playing():
            await asyncio.sleep(0.1)
        has_joined = True
    voice_client.play(discord.FFmpegPCMAudio(executable=FFMPEG_PATH, source=sound_names.SOUND_NAMES[sound_name] if sound_name in sound_names.SOUND_NAMES else sound_name))


def get_nick_or_name(member: discord.Member):
    if type(member) == discord.Member and member.nick != None:
        return member.nick
    return member.name


def run_discord_bot():
    sound_names.load_sounds(sound_names.SOUNDS_NAMES_FILE)

    TOKEN = open("../token.txt", 'r').readline().strip()
    PREFIX = "/?"
    
    intents = discord.Intents.all()
    intents.message_content = True
    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"{client.user} is now running!")

    @client.event
    async def on_message(message: discord.Message):
        global has_joined, is_ben
        
        if message.author == client.user:
            return
        
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        # print(f"{username} said: \"{user_message}\" in {channel}")

        if user_message.startswith(PREFIX):
            user_message = user_message[len(PREFIX):].lower()
            if user_message == "кыш":
                await voice_client.disconnect()
                is_ben = False
                has_joined = False
            elif user_message == "список":
                sound_names.load_sounds(sound_names.SOUNDS_NAMES_FILE)
                await message.channel.send('\n'.join(sound_names.SOUND_NAMES.keys()))
            elif user_message == "рулетка":
                res = ""
                members_ids = message.author.voice.channel.voice_states.keys()
                for member_id in members_ids:
                    name = get_nick_or_name(message.guild.get_member(member_id))
                    res += name + "\t" + random.choice([" сдаст", " не сдаст"]) + '\n'
                await message.channel.send(res)
            elif user_message == "число":
                res = ""
                members_ids = message.author.voice.channel.voice_states.keys()
                for member_id in members_ids:
                    name = get_nick_or_name(message.guild.get_member(member_id))
                    res += name + "\t" + str(random.randint(0, 99)) + '\n'
                await message.channel.send(res)
            elif user_message == "см":
                res = ""
                members_ids = message.author.voice.channel.voice_states.keys()
                for member_id in members_ids:
                    name = get_nick_or_name(message.guild.get_member(member_id))
                    res += name + "\t8" + '=' * random.randint(0, 150) + '>\n'
                await message.channel.send(res)
            elif user_message == "помощь":
                await message.channel.send("Напиши /?список, чтобы получить список доступных звуков.\nИли /?рулетка, чтобы узнать, кто сдаст экзамен.\n/?число, чтобы всё разрулить.")
            elif user_message == "?":
                if not is_ben:
                    await play_sound(message.author.voice.channel, sound_names.SOUNDS_NAMES_FILE + "/" + "бен.mp4")
                    while voice_client.is_playing():
                        await asyncio.sleep(0.1)
                    is_ben = True
                await play_sound(message.author.voice.channel, random.choice([sound_names.SOUNDS_NAMES_FILE + "/" + "да.mp4", sound_names.SOUNDS_NAMES_FILE + "/" + "нет.mp4", sound_names.SOUNDS_NAMES_FILE + "/" + "хохохо.mp4", sound_names.SOUNDS_NAMES_FILE + "/" + "ээы.mp4"]))
            elif user_message == "пинг":
                await message.channel.send("Понг!")
            elif user_message.startswith("гонка"):
                await message.channel.send("Гонщики, на старт!")
                for (index, attachment) in enumerate(message.attachments):
                    await attachment.save(f"player_icons/icon{index}.png")
                player_names = user_message.split()[1:]
                if len(player_names) == 0:
                    if len(message.attachments) == 0:
                        members_ids = message.author.voice.channel.voice_states.keys()
                        for (index, member_id) in enumerate(members_ids):
                            avatar = message.guild.get_member(member_id).avatar
                            if avatar is not None:
                                await avatar.save(f"player_icons/icon{index}.png")
                            name = get_nick_or_name(message.guild.get_member(member_id))
                            player_names.append(name)
                    else:
                        player_names = ["" for _ in range(len(message.attachments))]
                race_main.start(player_names)
                await message.channel.send("", file=discord.File("output.mp4"))
            elif user_message == "мегагонка":
                player_names = []
                await message.channel.send("Гонщики, на старт!")
                for (index, member) in enumerate(message.guild.members):
                    if member.avatar != None:
                        await member.avatar.save(f"player_icons/icon{index}.png")
                    name = get_nick_or_name(member)
                    player_names.append(name)
                race_main.start(player_names)
                await message.channel.send("", file=discord.File("output.mp4"))
            elif user_message in sound_names.SOUND_NAMES:
                is_ben = False
                await play_sound(message.author.voice.channel, user_message)
            else:
                await message.channel.send(f"Сам {user_message}!")

    client.run(TOKEN)
