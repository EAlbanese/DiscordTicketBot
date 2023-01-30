import configparser
import math
from datetime import datetime

# import database as database
from discord import (ApplicationContext, Bot, Embed,
                     EmbedField, Member, Option, Permissions, Button, PartialEmoji)
# from enums import PunishmentType
from pytimeparse.timeparse import timeparse
from view import SupportTicketCreateView, SupportModal, TeamComplaintModal, ApplicationModal

config = configparser.ConfigParser()
config.read("config.ini")

TOKEN = config.get('Bot', 'Token')
DEBUG_GUILDS = None if config.get('Bot', 'DebugGuilds') == "" else list(
    map(lambda id: int(id), config.get('Bot', 'DebugGuilds').split(',')))

bot = Bot(debug_guild=DEBUG_GUILDS)
# db = database.Database("bot.db")

# db.create_tables()


@bot.event
async def on_ready():
    print(f'{bot.user} is connected')


# Ticket System
@bot.slash_command(description="supportticket")
async def suppticket(interaction: ApplicationContext):
    embed = Embed(
        title=f'Support Tickets',
        description='Falls du Hilfe brauchst, jemanden melden oder dich Bewerben möchtest, dann öffne eines der folgenden Tickets. Ein Teammitglied wird in kürze bei dir sein.',
    )
    await interaction.respond("Created ticket embed", ephemeral=True)
    await interaction.channel.send(embed=embed, view=SupportTicketCreateView())


# @bot.slash_command(description="adminticket")
# async def adminsuppticket(interaction: ApplicationContext):
#     embed = Embed(
#         title=f'Admin Ticket',
#         description='If you need help, feel free to open one of the following tickets. A team admin will be with you in no time.',
#     )
#     await interaction.respond("Created ticket embed", ephemeral=True)
#     await interaction.channel.send(embed=embed, view=AddminTicketCreatView())

bot.run(TOKEN)
# db.connection.close()
