from typing import Literal, Optional

import discord
from discord.ext import commands
from cogs import EXTENSIONS
import logging
import os
from dotenv import load_dotenv
load_dotenv()

logging.getLogger("discord.gateway").setLevel(logging.WARNING)

intents = discord.Intents.all()

client = commands.Bot(command_prefix='?', intents=intents)

@client.event
async def on_ready():
    print(f'\u001b[1;32m{client.user.name} has connected and is now running.\u001b[0m')

    for extension in EXTENSIONS:
        await client.load_extension(extension)
        print(f'\u001b[1;32m{extension} has been loaded.\u001b[0m')

@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
    
    for extension in EXTENSIONS:
        await client.reload_extension(extension)
        print(f'\u001b[1;32m{extension} has been reloaded and synced.\u001b[0m')

    if not guilds:
        if spec == "~":
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

        await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
        )
        return

    ret = 0
    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            ret += 1

    await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

client.run(os.getenv("TOKEN"))