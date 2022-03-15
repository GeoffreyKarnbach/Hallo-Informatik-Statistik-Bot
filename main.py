from discord.ext import commands

bot = commands.Bot(command_prefix='!')

bot.load_extension("cogs.MessageGetter")

with open("Token.txt","r") as f:
    bot.run(f.readline().strip())
