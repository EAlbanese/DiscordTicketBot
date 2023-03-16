import configparser
import math
from datetime import datetime

import database as database
from discord import (ApplicationContext, Bot, Embed,
                     EmbedField, Member, Option, Permissions, Button, PartialEmoji, Activity, ActivityType, Thread)
# from enums import PunishmentType
from pytimeparse.timeparse import timeparse
from view import SupportTicketCreateView, SupportModal, TeamComplaintModal, BewerbungModal, BugReportCreateView, SuggestionView, WishView

config = configparser.ConfigParser()
config.read("config.ini")

TOKEN = config.get('Bot', 'Token')
DEBUG_GUILDS = None if config.get('Bot', 'DebugGuilds') == "" else list(
    map(lambda id: int(id), config.get('Bot', 'DebugGuilds').split(',')))

bot = Bot(debug_guild=DEBUG_GUILDS)
db = database.Database("bot.db")

# db.drop_ticketdb()
db.create_ticket_table()


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
        description='Hier findest du alle Commands, welche der Bot kann und wie du diese ausführen kannst.',
    )
    embed.add_field(name="Bug melden", value="Mit ``/bugreport`` kannst du einen Bug melden. Ich bitte dich, sobald du einen Fehler oder Bug gefunden hast, den zu melden!", inline=False)
    embed.add_field(name="Verbesserungsvorschläge",
                    value="Mit ``/suggestion`` kannst du mir Verbesserungsvorschläge mitteilen. Ich freue mich über jegliches Feedback von euch.", inline=False)
    embed.add_field(name="Wünsche",
                    value="Mit ``/wish`` kannst du mir deinen Wunsch mitteilen. Ich werde mir deinen Wunsch anschauen und mich mit dir in Kontakt setzten.", inline=False)
    embed.add_field(name="Sonstige Hilfe",
                    value="Du kannst mir auch jederzeit via Discord DM --> **Draixon#1999** ein Feedback geben oder Fragen über den Bot stellen.", inline=False)

    await interaction.respond("Hilfe ist unterwegs!", ephemeral=True)
    await interaction.channel.send(embed=embed)


# Bug report
@bot.slash_command(description="Bug reporten")
async def bugreport(interaction: ApplicationContext):
    embed = Embed(
        title=f'Hast du einen Bug gefunden?',
        description='Falls du einen Bug gefunden hast, bitte ich dich den genau zu beschreiben. \n \n ❗Falls es doch kein Bug ist, dann bitte ich dich auf **Abbrechen** zu drücken.',
    )
    await interaction.respond("Danke für das melden!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=BugReportCreateView())


# Suggestion
@bot.slash_command(description="Verbesserungsvorschlag")
async def suggestion(interaction: ApplicationContext):
    embed = Embed(
        title=f'Hast du einen Verbesserungsvorschlag?',
        description='Falls du einen Verbesserungsvorschlag hast, kannst du mir diesen jederzeit mitteilen.',
    )
    await interaction.respond("Danke für den Vorschlag!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=SuggestionView())


# Wish
@bot.slash_command(description="Wünsche")
async def wish(interaction: ApplicationContext):
    embed = Embed(
        title=f'Hast du einen Wunsch?',
        description='Falls du einen Wunsch hast, kannst du mir diesen jederzeit mitteilen.',
    )
    await interaction.respond("Danke für deinen Wunsch!", ephemeral=True)
    await interaction.channel.send(embed=embed, view=WishView())


bot.run(TOKEN)
db.connection.close()
