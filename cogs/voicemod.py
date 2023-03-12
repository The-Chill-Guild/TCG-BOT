import discord
from discord.ext import commands

class VoiceMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('✅ VoiceMod.py is loaded.')

    @commands.command()
    async def whichvoice(self, ctx, member: discord.Member):
        if member.voice is None:
            await ctx.send(f"{member.name} is not in a voice channel.")
        else:
            await ctx.send(f"{member.name} is in voice channel <#{member.voice.channel.id}>")

    @commands.command()
    async def move(self, ctx, member: discord.Member, channel: discord.VoiceChannel):
        await member.move_to(channel)
        await ctx.send(f"{member.name} has been moved to {channel.name}")

    @commands.command()
    async def deafen(self, ctx, member: discord.Member):
        await member.edit(deafen=True)
        await ctx.send(f"{member.name} has been deafened.")

    @commands.command()
    async def undeafen(self, ctx, member: discord.Member):
        await member.edit(deafen=False)
        await ctx.send(f"{member.name} has been undeafened.")

    @commands.command()
    async def mute(self, ctx, member: discord.Member):
        await member.edit(mute=True)
        await ctx.send(f"{member.name} has been muted.")

    @commands.command()
    async def unmute(self, ctx, member: discord.Member):
        await member.edit(mute=False)
        await ctx.send(f"{member.name} has been unmuted.")

async def setup(bot):    
    await bot.add_cog(VoiceMod(bot))