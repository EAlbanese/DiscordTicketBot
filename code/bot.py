import configparser
import math
from datetime import datetime

import database as database
from discord import (ApplicationContext, Bot, Embed,
                     EmbedField, Member, Option, Permissions, Button, PartialEmoji, Activity, ActivityType, Thread)
# from enums import PunishmentType
from pytimeparse.timeparse import timeparse
from view import SupportTicketCreateView, SupportModal, TeamComplaintModal, ApplicationModal, BugReportCreateView

config = configparser.ConfigParser()
config.read("config.ini")

TOKEN = config.get('Bot', 'Token')
DEBUG_GUILDS = None if config.get('Bot', 'DebugGuilds') == "" else list(
    map(lambda id: int(id), config.get('Bot', 'DebugGuilds').split(',')))

bot = Bot(debug_guild=DEBUG_GUILDS)
db = database.Database("bot.db")

# db.drop_db()
db.create_tables()


@bot.event
async def on_ready():
    print(f'{bot.user} is connected')
    await bot.change_presence(activity=Activity(type=ActivityType.watching, name="/help für Hilfe"))


# Ticket System
@bot.slash_command(description="Erstellt das Ticket Embed")
async def ticket(interaction: ApplicationContext):
    embed = Embed(
        title=f'Support Tickets',
        description='Falls du Hilfe brauchst, jemanden melden oder dich Bewerben möchtest, dann öffne eines der folgenden Tickets. Ein Teammitglied wird in kürze bei dir sein. \n \n ⛔ Für das missbrauchen des Ticket-Systems gibt es Verwarnungen.',
    )
    await interaction.respond("Created ticket embed", ephemeral=True)
    await interaction.channel.send(embed=embed, view=SupportTicketCreateView())

# Help


@bot.slash_command(description="Ticket System Command-Liste")
async def help(interaction: ApplicationContext):
    embed = Embed(
        title=f'Hilfe',
        description='Hier findest du alle Commands, welche der Bot kann und wie du diese ausführen kannst. \n \n ❗Falls es doch kein Bug ist, dann bitte ich dich auf **Abbrechen** zu drücken.',
    )

    await interaction.respond("Hilfe ist unterwegs!", ephemeral=True)
    await interaction.channel.send(embed=embed)


# Bug report
@bot.slash_command(description="Bug reporten")
async def bugreport(interaction: ApplicationContext):
    embed = Embed(
        title=f'Hast du ein Bug gefunden?',
        description='Falls du einen Bug gefunden hast, bitte ich dich den genau zu beschreiben.',
    )
    await interaction.respond("Danke für das melden!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=BugReportCreateView())


bot.run(TOKEN)
db.connection.close()
