import discord
from discord.ext import commands
import asyncio

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('✅ Moderation.py is loaded.')
# clear command
    @commands.command(alias=['purge'])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount:int):
        await ctx.channel.purge(limit=1+amount)
        await ctx.send(f'**{amount}** messages have been deleted.')
        await asyncio.sleep(3)
        await ctx.channel.purge(limit=1)
        

# ban command
    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str):
        await member.ban(reason=reason)
        await ctx.send(f'**{member}** has been banned.')

        conf_embed = discord.Embed(title='Success', color=discord.Color.red())
        conf_embed.add_field(name='User Banned', value=f'{member.mention} has been banned by {ctx.author.mention}.', inline=False)
        conf_embed.add_field(name='Reason', value=f'{reason}', inline=False)
        await ctx.send(embed=conf_embed)

# kick command
    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str):
        await member.kick(reason=reason)
        await ctx.send(f'**{member}** has been kicked.')

        conf_embed = discord.Embed(title='Success', color=discord.Color.yellow())
        conf_embed.add_field(name='User Kicked', value=f'{member.mention} has been kicked by {ctx.author.mention}.', inline=False)
        conf_embed.add_field(name='Reason', value=f'{reason}', inline=False)
        await ctx.send(embed=conf_embed)

# unban command
    @commands.command(name='unban')
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def unban(self ,ctx ,userId):
        user = discord.Object(id=userId)
        await ctx.guild.unban(user)

        conf_embed = discord.Embed(title='Success', color=discord.Color.green())
        conf_embed.add_field(name='User Unbanned', value=f'<@{userId}> has been unbanned by {ctx.author.mention}.', inline=False)
        await ctx.send(embed=conf_embed)

async def setup(bot):
    await bot.add_cog(Moderation(bot))
