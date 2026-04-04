from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
import random
import time
import asyncio

#VERSION
version = "4.3.5"

#1. Load token
load_dotenv() 
token = os.getenv("token")

#2. Description of Bot
description = """The Potato Bot with useful commands!"""

#3. Initialize Bot
bot = commands.Bot(command_prefix='.', description=description, self_bot=False)

#Register on_ready
@bot.event
async def on_ready():
    print('---------------------------')
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('---------------------------')
    channel = bot.get_channel(1486218054265213029)  # channel ID
    await channel.send('PotatoBot version ' + version + ' is online and ready to serve you!')


#-------COMMANDS------------
commands = [
    {
        "name": "potatobotversion",
        "description": "Displays the current version of PotatoBot. Current version is " + version,
        "usage": ".potatobotversion"
    },
    {
        "name": "add",
        "description": "Adds two numbers together.",
        "usage": ".add <number1> <number2>"
    },
    {
        "name": "choose",
        "description": "Choose from your given options.",
        "usage": ".choose <option1> <option2> ... <optionN>"
    },
    {
        "name": "repeat",
        "description": "Spammer muahahah.",
        "usage": ".repeat <times> [content]"
    },
    {
        "name": "joined",
        "description": "Says when a member joined.",
        "usage": ".joined @member"
    },
    {
        "name": "spammer",
        "description": "Toggles spamming of timestamps every 2 seconds.",
        "usage": ".spammer <true|false>"
    },
    {
        "name": "cool",
        "description": "Says if a user is cool. Use subcommand 'bot' to check if the bot is cool.",
        "usage": ".cool [subcommand]"
    }
]

@bot.command()
async def potatobothelp(ctx):
    """Displays a list of available commands and their descriptions."""
    help_message = "Here are the available commands:\n\n"
    for cmd in commands:
        help_message += f"**{cmd['name']}**: {cmd['description']}\nUsage: `{cmd['usage']}`\n\n"
    await ctx.send(help_message)

@bot.command()
async def potatobotversion(ctx):
    """Displays the current version of PotatoBot."""
    await ctx.send('PotatoBot version' + version)

@bot.command()
async def add(ctx, left: int, right: int):
    """Adds two numbers together."""
    await ctx.send(left + right)


@bot.command(description='Choose from your given options')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))


@bot.command(description='Spammer muahahah')
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)


@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined in {member.joined_at}')


spamming = False
@bot.command()
async def spammer(ctx, toggle: bool):
    global spamming
    spamming = toggle

    while spamming:
        await ctx.send(str(int(time.time() * 1000)))
        await asyncio.sleep(2)  


@bot.group()
async def cool(ctx):
    """Says if a user is cool.

    In reality this just checks if a subcommand is being invoked.
    """
    if ctx.invoked_subcommand is None:
        await ctx.send(f'Yes, {ctx.subcommand_passed} is cool!')


@cool.command(name='bot')
async def _bot(ctx):
    """Is the bot cool?"""
    await ctx.send('Yes, the bot is cool.')


bot.run(str(token))



#-----Bot Events for Poke-Name Bot-----
POKENAME_BOT_ID = 874910942490677270  # replace with Poke-Name bot ID
SPAWN_CHANNEL_IDS = {
    1488335877863379055,  # spawn1
    1487301631958585515,  # spawn2
    1487303738044583956,  # spawn3
    1488321278526885899,  # spawn4
    1488321292355502200,  # spawn5
    1488321339860193360,  # spawn6
    1488321350014734347,  # spawn7
    1488321382789157016,  # spawn8
    1488321394663100516,  # spawn9
    1488321402456248383,  # spawn10
}

locked_channels = set()

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

@bot.event
async def on_message(message):
    await bot.process_commands(message)

    if message.author.id != POKENAME_BOT_ID:
        return

    if message.channel.id not in SPAWN_CHANNEL_IDS:
        return

    if message.channel.id in locked_channels:
        return

    if "Collection Pings:" not in message.content:
        return

    if not message.mentions:
        return

    channel = message.channel
    guild = message.guild
    everyone = guild.default_role

    locked_channels.add(channel.id)

    try:
        await channel.send("[testing]A Pokémon has spawned! You have 30 seconds to catch it!")
        everyone_overwrite = channel.overwrites_for(everyone)
        old_everyone_send = everyone_overwrite.send_messages

        everyone_overwrite.send_messages = False
        await channel.set_permissions(everyone, overwrite=everyone_overwrite)

        temp_overwrites = {}

        for user in message.mentions:
            member = guild.get_member(user.id)
            if member is None:
                continue

            member_overwrite = channel.overwrites_for(member)
            temp_overwrites[member.id] = member_overwrite.send_messages

            member_overwrite.send_messages = True
            await channel.set_permissions(member, overwrite=member_overwrite)

        await asyncio.sleep(30)

        for user in message.mentions:
            member = guild.get_member(user.id)
            if member is None:
                continue

            previous_value = temp_overwrites.get(member.id, None)
            member_overwrite = channel.overwrites_for(member)
            member_overwrite.send_messages = previous_value

            if member_overwrite.is_empty():
                await channel.set_permissions(member, overwrite=None)
            else:
                await channel.set_permissions(member, overwrite=member_overwrite)

        everyone_overwrite = channel.overwrites_for(everyone)
        everyone_overwrite.send_messages = old_everyone_send

        if everyone_overwrite.is_empty():
            await channel.set_permissions(everyone, overwrite=None)
        else:
            await channel.set_permissions(everyone, overwrite=everyone_overwrite)

    finally:
        locked_channels.discard(channel.id)

bot.run(str(token))
