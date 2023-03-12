import discord
from discord.ext import commands

class Utility(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('✅ Utility.py is loaded.')

#ping command
    @commands.command(aliases=['latency', 'Ping',])
    async def ping(self, ctx):
        await ctx.send('Pong! {0}ms'.format(round(self.bot.latency * 1000)))

#avatar command
    @commands.command(aliases=['av', 'pfp', 'Avatar', 'Av', 'Pfp', 'PFP', 'AVATAR'])
    async def avatar(self, ctx, member: discord.Member=None):
        member = member or ctx.author
        avatar_url = member.avatar.url
        await ctx.send(avatar_url)


async def setup(bot):
   await bot.add_cog(Utility(bot))