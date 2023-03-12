import discord
from discord.ext import commands
import random
import asyncio

class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print('✅ Fun.py is loaded.')

    @commands.command()
    async def gtn(self, ctx):
        await ctx.send('Guess a number between 1 and 50.')

        def is_correct(m):
            return m.author == ctx.author and m.content.isdigit()

        answer = random.randint(1, 50)

        try:
            guess = await self.client.wait_for('message', check=is_correct, timeout=5.0)
        except asyncio.TimeoutError:
            return await ctx.send('Sorry, you took too long it was {}.'.format(answer))

        if int(guess.content) == answer:
            await ctx.send('You are right!')
        else:
            await ctx.send('Sorry. It is actually {}.'.format(answer))

    @commands.command()
    async def rps(self, ctx, choice: str):
        choices = ['r', 'p', 's']
        bot_choice = random.choice(choices)
        author_choice = choice.lower()
        if author_choice == bot_choice:
            await ctx.send(f'Both players selected {author_choice}. It\'s a tie!')
        elif author_choice == 'r':
            if bot_choice == 's':
                await ctx.send('Rock smashes scissors! You win!')
            else:
                await ctx.send('Paper covers rock! You lose.')
        elif author_choice == 'p':
            if bot_choice == 'r':
                await ctx.send('Paper covers rock! You win!')
            else:
                await ctx.send('Scissors cuts paper! You lose.')
        elif author_choice == 's':
            if bot_choice == 'p':
                await ctx.send('Scissors cuts paper! You win!')
            else:
                await ctx.send('Rock smashes scissors! You lose.')
        else:
            await ctx.send('Please enter a valid move!')

    @commands.command(aliases=['coin', 'flip', 'Coin', 'Flip', 'COIN', 'FLIP','cf','CF'])
    async def coinflip(self, ctx):
        choices = ['Heads', 'Tails']
        await ctx.send(f'{random.choice(choices)}')

#8ball command
    @commands.command(aliases=['8ball', '8Ball', '8BALL'])
    async def _8ball(self, ctx, *, question):
        responses = ['It is certain.',
                     'It is decidedly so.',
                     'Without a doubt.',
                     'Yes - definitely.',
                     'You may rely on it.',
                     'As I see it, yes.',
                     'Most likely.',
                     'Outlook good.',
                     'Yes.',
                     'Signs point to yes.',
                     'Reply hazy, try again.',
                     'Ask again later.',
                     'Better not tell you now.',
                     'Cannot predict now.',
                     'Concentrate and ask again.',
                     'Don\'t count on it.',
                     'My reply is no.',
                     'My sources say no.',
                     'Outlook not so good.',
                     'Very doubtful.']
        await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


async def setup(client):
    await client.add_cog(Fun(client))