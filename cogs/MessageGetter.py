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
    
    @commands.command()
    async def get_user_ranking(self, ctx):
        messages = {}
        channel_nb = len(ctx.message.guild.text_channels)
        msg_ = await ctx.send(f"Start checking 0/{channel_nb}")
        counter = 0
        total = 0
        total_counter = await ctx.send(f"Messages checked: 0")

        for channel in ctx.message.guild.text_channels:
            counter += 1
            async for message in channel.history(limit = None):
                total+=1
                if total % 1000 == 0:
                    await total_counter.edit(content = f"Checked {total} messages.")
                if message.author.id in messages:
                    messages[message.author.id]+=1
                else:
                    messages[message.author.id]=1
            await msg_.edit(content = f"Checking {counter}/{channel_nb}")
        
        await ctx.send(f"Total of {len(messages)} messages found")
 
        with open("messages.txt","w", encoding="utf-8") as f:
            for elem in sorted(messages.items(), key=lambda x: x[1], reverse=True):
                '''
                try:
                    member = await self.client.fetch_user(elem[0])
                except:
                    member = "ERROR"
                '''
                f.write(f"{elem[0]} - {elem[1]}\n")

        with open("messages.txt", "rb") as file:
            await ctx.send("List of all messages:", file=discord.File(file, "messages.txt"))
    
    @commands.command()
    async def associate(self, ctx):
        
        with open("messages.txt","r") as f:
            liste = [elem.strip().split("-") for elem in f.readlines()]
        counter = 0
        message = await ctx.send(f"Converting {counter}/{len(liste)}")

        with open("new_messages.txt","w", encoding="utf-8") as f:
            for user, number in liste:
                counter+=1
                try:
                    user_ = await self.client.fetch_user(int(user.strip()))
                    f.write(f"{user_.name}#{user_.discriminator} - {number}\n")
                except:
                    f.write(f"{user} - {number}\n")
                await message.edit(content = f"Converting {counter}/{len(liste)}")
        
        with open("new_messages.txt", "rb") as file:
            await ctx.send("List of all messages:", file=discord.File(file, "messages.txt"))



    
def setup(client):
    client.add_cog(MessageGetter(client))

