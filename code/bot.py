import configparser
import math
from datetime import datetime

import database as database
from discord import (ApplicationContext, Bot, Embed,
                     EmbedField, Member, Option, Permissions, Button, PartialEmoji, Activity, ActivityType, Thread)
# from enums import PunishmentType
from pytimeparse.timeparse import timeparse
from view import SupportTicketCreateView, SupportModal, TeamComplaintModal, ApplicationModal

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
    await bot.change_presence(activity=Activity(type=ActivityType.watching, name="your Tickets"))


# Ticket System
@bot.slash_command(description="Erstellt das Ticket Embed")
async def ticket(interaction: ApplicationContext):
    embed = Embed(
        title=f'Support Tickets',
        description='Falls du Hilfe brauchst, jemanden melden oder dich Bewerben möchtest, dann öffne eines der folgenden Tickets. Ein Teammitglied wird in kürze bei dir sein. \n \n ⛔ Für das missbrauchen des Ticket-Systems gibt es Verwarnungen.',
    )
    await interaction.respond("Created ticket embed", ephemeral=True)
    await interaction.channel.send(embed=embed, view=SupportTicketCreateView())


@bot.slash_command(description="Geschlossenes Ticket wird eröffnet")
async def reopen(interaction: ApplicationContext, ticketid: Option(str,  "Ticket Id eingeben")):

    thread = interaction.guild.get_thread(int(ticketid))

    await thread.edit(archived=False, locked=False)
    await interaction.respond(f"<#{thread.id}> Ticket wurde wieder geöffnet", ephemeral=True)

bot.run(TOKEN)
db.connection.close()
