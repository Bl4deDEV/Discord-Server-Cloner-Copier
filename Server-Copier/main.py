import requests
import discord 
import os
os.system('cls')
token = input(" \033[36m Enter the Discord Token to Login => ")

client = discord.Client(intents=discord.Intents.all())

async def copy_server(guildId: int, servertocopy: int):
    guild = client.get_guild(guildId)
    copy = client.get_guild(servertocopy)
    for channel in guild.channels:
        await channel.delete()
    for category in copy.categories:
       try:
        cate = await guild.create_category(name=category.name)
        for channel in category.channels:
            if isinstance(channel, discord.VoiceChannel):
                await cate.create_voice_channel(name=channel.name)
            if isinstance(channel, discord.StageChannel):
                await cate.create_stage_channel(name=channel.name)
            if isinstance(channel, discord.TextChannel):
                await cate.create_text_channel(name=channel.name)
       except:
           pass
    try:
        await guild.edit(icon=copy.icon_url, name=copy.name)
    except:
        pass

async def get_channel_history(channel_id):
    channel = client.get_channel(int(channel_id))
    msgs = []
    messages = await channel.history(limit=100).flatten()
    for i in range(len(messages)):
        for attachment in messages[i].attachments:
            msgs.append(attachment.url)
    return msgs

def name() -> str:
    return requests.get('https://discord.com/api/v9/users/@me', headers={"Authorization": token}).json()['username']

async def Menu():
    os.system("cls & title Server Steal")
    print(f"""
    
    \t\t\t    ____ ____ ____ _  _ ____ ____    ____ ___ ____ ____ _    
    \t\t\t    [__  |___ |__/ |  | |___ |__/    [__   |  |___ |__| |    
    \t\t\t    ___] |___ |  \  \/  |___ |  \    ___]  |  |___ |  | |___ 
                                             [+] {name()}  [+]
[1] - Steal Messages
[2] - Copy Server
[3] - CREDITS https://github.com/@Bl4deDEV/
   """)
    cmd = input("? ")
    if cmd == "1":
        channel_id = input("Channel ID To Scrape => ")
        messages = await get_channel_history(int(channel_id))
        print(f"Scraped {len(messages)} attachment{'s' if len(messages) != 1 else ''}")
        scrape_channel = input("Channel ID To Send Scrape To => ")
        for message in messages:
           try:
            channel = client.get_channel(int(scrape_channel))
            await channel.send(message)
            print(f"[SUCCESSFUL] uploaded an image to {scrape_channel}")
           except:
               print(f"[FAILURE] failed to upload an image to {scrape_channel}")
        await Menu()
    elif cmd == "2":
        guild = int(input("Your Server ID=> "))
        copy = int(input("Server ID To Copy => "))
        await copy_server(guild, copy)
    else:
        await Menu()

@client.event
async def on_ready():
    await Menu()


if __name__ == '__main__':
    try:
        client.run(token, bot=False)
    except:
        os._exit(0)
