import discord
from discord.ext import commands


class MessageGetter(commands.Cog):

    def __init__(self,client):
        self.client = client

    
    @commands.Cog.listener()
    async def on_ready(self):
        print("Bot is ready")
    

    @commands.command()
    async def get_messages_from(self, ctx, member: discord.Member):
        messages = []
        channel_nb = len(ctx.message.guild.text_channels)
        msg_ = await ctx.send(f"Start checking 0/{channel_nb}")
        counter = 0
        total = 0

        for channel in ctx.message.guild.text_channels:
            counter += 1
            async for message in channel.history(limit = None):
                total += 1
                if message.author == member:
                    messages.append(message)
            await msg_.edit(content = f"Checking {counter}/{channel_nb}")
        
        await ctx.send(f"Total of {len(messages)} messages found")
        await ctx.send(f"Total messages: {total}")

        with open("messages.txt","w", encoding="utf-8") as f:
            for msg in messages:
                f.write(msg.content+"\n")

        with open("messages.txt", "rb") as file:
            await ctx.send("List of all messages:", file=discord.File(file, "messages.txt"))

    
def setup(client):
    client.add_cog(MessageGetter(client))

