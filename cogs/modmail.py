import discord
from discord.ext import commands
import sqlite3
from datetime import datetime


class ModMail(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print('✅ ModMail.py is loaded.')

db = sqlite3.connect('modmail.db')
cursor = db.cursor()
# Must run this snippet only once then comment it
cursor.execute("""
     CREATE TABLE modmail (
         user_id int,
         channel_id int
      )
""")

def check(key):
    if key is None:
        return False
    else:
        return True


@commands.Cog.listener()
async def on_message(self,  message : discord.Message):
    guild = self.bot.get_guild(1084054406879772682)
    category = self.bot.get_channel(1084067281920856135)
    admin_role = discord.utils.get(guild.roles, name="ModMail Support")

    if message.author == self.bot.user:
        return
    
    if not message.guild:
        cursor.execute("SELECT user_id FROM modmail WHERE user_id = (?)", (message.author.id, ))
        if check(cursor.fetchone()) is True:
            try:
                print("RETURNING USER")
                cursor.execute("SELECT channel_id FROM modmail WHERE user_id = (?)", (message.author.id, ))
                channel_id = cursor.fetchone()
                for id in channel_id:
                    channel_id = id
                    break
                channel = self.bot.get_channel(channel_id)
                if channel is None:
                    print("CHANNEL NOT FOUND")
                    overwrites = {
                        guild.default_role : discord.PermissionOverwrite(read_messages=False),
                        admin_role : discord.PermissionOverwrite(read_messages=True)
                    }
                    new_channel = await message.guild.create_text_channel(f"{message.author.name}", overwrites=overwrites, category=category)

                    cursor.execute("UPDATE modmail SET channel_id = (?) WHERE user_id = (?)", (new_channel.id, message.author.id, ))
                    db.commit()
                    channel = new_channel
                
                await channel.send(message.content)
            except Exception as e:
                print(e)
                await message.add_reaction('❌')
                
        else:
            try:
                print("NEW USER")
                overwrites = {
                    guild.default_role : discord.PermissionOverwrite(read_messages=False),
                    admin_role : discord.PermissionOverwrite(read_messages=True)
                }

                modmail_channel = await message.guild.create_text_channel(f"{message.author.name}", overwrites=overwrites, category=category)

                cursor.execute("INSERT INTO modmail VALUES (?, ?)", (message.author.id, modmail_channel.id, ))
                db.commit()
                sembed = discord.Embed(
                    title="Thank you for contacting the support team!",
                    color = discord.colour.Color.default(),
                    timestamp=datetime.now(),
                    description="We will get back to you as soon as possible."
                )
                sembed.set_thumbnail(url=guild.icon.url)
                await message.author.send(embed=sembed)
                embed = discord.Embed(
                    title="New Modmail Ticket",
                    color = discord.colour.Color.brand_green(),
                    timestamp=datetime.now(),
                    description=message.content
                )
                embed.set_footer(icon_url=message.author.avatar.url, text='\
                    Sent by {}'.format(message.author.name))
                embed.set_author(name=message.author.name, icon_url=message.author.avatar.url)
                await modmail_channel.send(embed=embed)
                
            except Exception as e:
                print(e)
                await message.add_reaction('❌')

    else:
        if message.channel.category == category:
            cursor.execute("SELECT channel_id FROM modmail WHERE user_id = (?)", (message.author.id, ))
            if check(cursor.fetchone()) is True:
                try:
                    cursor.execute("SELECT user_id FROM modmail WHERE channel_id = (?)", (message.channel.id, ))
                    user_id = cursor.fetchone()

                    for id in user_id:
                        user_id = id
                        break
                
                    user = discord.utils.get(guild.members, id=user_id)
                    if user is None:
                        await message.reply("I can't find that user ⚠")
                        await message.add_reaction('❌')
                        return
                    else:
                        if message.content == '!close':
                            close_embed = discord.Embed(
                                title="Ticket is Closed",
                                timestamp=datetime.now(),
                                color = discord.colour.Color.dark_red(),
                                description=f"This ticket is now closed and no longer being managed by the staff team, if you need anything else please feel free to shoot us another message and we'll get back to you as soon as we can."
                            )
                            close_embed.set_footer(text="By replying, you are opening another ticket")
                            await user.send(embed=close_embed)
                            channel = message.channel
                            await channel.delete()
                            cursor.execute("DELETE FROM modmail WHERE channel_id = (?)", (channel.id, ))
                            db.commit()
                        else:
                            await user.send(message.content)
                        await message.add_reaction('✅')
                except Exception as e:
                    print(e)
                    await message.add_reaction('❌')

async def setup(bot):
        await bot.add_cog(ModMail(bot))