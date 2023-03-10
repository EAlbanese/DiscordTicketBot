from discord import ui, ButtonStyle, InputTextStyle, Interaction, Embed, PermissionOverwrite, ChannelType, Client
import database as database
import datetime

client = Client()
db = database.Database("bot.db")


class variableManager(ui.View):
    threadID = 0

# Ticket System


class TicketManageView(ui.View):
    @ui.button(label="Ticket schliessen", style=ButtonStyle.primary)
    async def first_button_callback(self, button,  interaction: Interaction):
        channel = await interaction.guild.fetch_channel(1072160823088267314)

        thread = interaction.guild.get_thread(interaction.message.channel.id)

        ticketId = db.get_ticket_id_by_thread_id(
            interaction.message.channel.id)
        ticketinfo = db.get_ticket_info(ticketId)
        ticketClosedBy = interaction.user.display_name
        memberName = interaction.guild.get_member(ticketinfo[2])
        moderatorName = interaction.guild.get_member(ticketinfo[3])

        embed = Embed(title=f"๐ Ticket wurde geschlossen")
        embed.add_field(name="๐ซ Ticket ID",
                        value=f'{ticketinfo[0]}', inline=False)
        embed.add_field(name="๐ซ Thread ID",
                        value=f'{ticketinfo[1]}', inline=False)
        embed.add_field(name="๐ค Ticket geรถffnet von",
                        value=f'{memberName}', inline=False)
        embed.add_field(name="โ Ticket geclaimt von",
                        value=f'{moderatorName}', inline=False)
        embed.add_field(name="๐ Ticket geschlossen von",
                        value=f'{ticketClosedBy}', inline=False)

        await channel.send(embed=embed, view=TicketLogsView())
        await thread.edit(archived=True, locked=True)
        await interaction.response.defer()

    @ui.button(label="Claim Ticket", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction: Interaction):
        staffrole = interaction.guild.get_role(1070629289520807947)

        thread = interaction.guild.get_thread(interaction.message.channel.id)
        count = db.get_ticket_id_by_thread_id(interaction.message.channel.id)

        if staffrole not in interaction.user.roles:
            await interaction.response.send_message("โ Keine Berechtigung!", ephemeral=True)
            return
        db.update_claimed_ticket(interaction.user.id, count)
        embed = Embed(title="Ticket Status geรคndert: Wir sind dabei!",
                      description=f"<@{interaction.user.id}> kรผmmert sich um dein Ticket.")
        embed.author.name = interaction.user.display_name
        embed.author.icon_url = interaction.user.display_avatar
        await interaction.response.send_message(embed=embed)
        await thread.edit(name=f"{count} - {interaction.user.name}")


class TicketLogsView(ui.View):
    @ui.button(label="๐ Ticket erneut รถffnen", style=ButtonStyle.primary)
    async def reopenTicket(self, button,  interaction: Interaction):

        thread = interaction.guild.get_thread(
            int(interaction.message.embeds[0].fields[1].value))

        print(thread)

        await thread.edit(archived=False, locked=False)
        await interaction.response.send_message(f"<#{thread.id}> Ticket wurde wieder geรถffnet", ephemeral=True)


class SupportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Wo benรถtigst du Hilfe?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(
            title="Anliegen", description="โ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kรผmmern!")
        embed.add_field(name="Wo benรถtigst du Hilfe?",
                        value=self.children[0].value)
        channel = await interaction.guild.fetch_channel(1071005969359847464)

        create_date = datetime.datetime.now()

        print(create_date)

        test = db.create_ticket(interaction.user.id,
                                round(create_date.timestamp()))

        print(test)
        print("db-test")

        count = db.get_ticket_id(round(create_date.timestamp()))

        response = await channel.create_thread(name=f"{count} - {interaction.user.display_name}", type=ChannelType.private_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)

        db.update_ticket(variableManager.threadID, count)

        await interaction.response.send_message(f"Ticket erรถffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@&{1070629289520807947}>", embed=embed, view=TicketManageView())


class TeamComplaintModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Was fรผr eine Team Beschwerde hast du?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Team Beschwerde",
                      description="โ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kรผmmern!")
        embed.add_field(name="Was fรผr eine Team Beschwerde hast du?",
                        value=self.children[0].value)
        channel = await interaction.guild.fetch_channel(1071005969359847464)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, round(create_date.timestamp()))
        count = db.get_ticket_id(round(create_date.timestamp()))

        response = await channel.create_thread(name=f"{count} - {interaction.user.display_name}", type=ChannelType.private_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)

        db.update_ticket(variableManager.threadID, count)

        await interaction.response.send_message(f"Ticket erรถffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@&{1071486720849223792}>", embed=embed, view=TicketManageView())


class ApplicationModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Als was mรถchtest du dich bewerben?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Bewerbung",
                      description="โ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kรผmmern!")
        embed.add_field(
            name="Als was mรถchtest du dich bewerben?", value=self.children[0].value)

        channel = await interaction.guild.fetch_channel(1071005969359847464)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, round(create_date.timestamp()))
        count = db.get_ticket_id(round(create_date.timestamp()))

        response = await channel.create_thread(name=f"{count} - {interaction.user.display_name}", type=ChannelType.private_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)

        db.update_ticket(variableManager.threadID, count)

        await interaction.response.send_message(f"Ticket erรถffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@&{1070629289520807947}>", embed=embed, view=TicketManageView())


class SupportTicketCreateView(ui.View):
    @ ui.button(emoji="๐ฉ", label="Anliegen", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(SupportModal(title="Anliegen Ticket"))

    @ ui.button(emoji="๐ฉ", label="Team Beschwerde", style=ButtonStyle.danger)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_modal(TeamComplaintModal(title="Team Beschwerde"))

    @ ui.button(emoji="๐ฉ", label="Bewerbung", style=ButtonStyle.success)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_modal(ApplicationModal(title="Bewerbung"))


# Bug report
class BugReportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Dein Username (Username#0000)", style=InputTextStyle.short))
        self.add_item(ui.InputText(
            label="Bug Titel", style=InputTextStyle.short))
        self.add_item(ui.InputText(
            label="Wie oft ist das aufgetreten?", style=InputTextStyle.long))
        self.add_item(ui.InputText(
            label="Beschreibe dein Vorgehen bis zum Bug", style=InputTextStyle.short))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="โ Neuer Bug-Report โ")
        embed.add_field(
            name="Username", value=self.children[0].value, inline=False)
        embed.add_field(
            name="Bug Titel", value=self.children[1].value, inline=False)
        embed.add_field(
            name="Beschreibe dein Vorgehen bis zum Bug", value=self.children[2].value, inline=False)
        embed.add_field(
            name="Wie oft ist das aufgetreten?", value=self.children[3].value, inline=False)

        draixon = await interaction.client.fetch_user(479537494384181248)

        await interaction.response.send_message(f"โ Bug wurde erfolgreich gemeldet. Vielen Dank โค๏ธ", ephemeral=True)
        await draixon.send(embed=embed)
        await interaction.message.delete()


class BugReportCreateView(ui.View):
    @ui.button(emoji="๐๏ธ", label="Abbrechen", style=ButtonStyle.danger)
    async def cancel_bugreport(self, button, interaction: Interaction):
        await interaction.message.delete()

    @ui.button(emoji="๐ฌ", label="Bug melden", style=ButtonStyle.success)
    async def report_bug(self, button, interaction):
        await interaction.response.send_modal(BugReportModal(title="Bug melden"))


# Suggestion
class SuggestionModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Dein Username (Username#0000)", style=InputTextStyle.short))
        self.add_item(ui.InputText(
            label="Verbesserungsvorschlag Titel", style=InputTextStyle.short))
        self.add_item(ui.InputText(
            label="Was kann ich verbesser?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="๐?๏ธ Neuer Verbesserungsvorschlag ๐?๏ธ")
        embed.add_field(
            name="Username", value=self.children[0].value, inline=False)
        embed.add_field(
            name="Verbesserungsvorschlag Titel", value=self.children[1].value, inline=False)
        embed.add_field(
            name="Was kann ich verbesser?", value=self.children[2].value, inline=False)

        draixon = await interaction.client.fetch_user(479537494384181248)

        await interaction.response.send_message(f"โ Vorschlag wurde erfolgreich eingereicht. Vielen Dank โค๏ธ", ephemeral=True)
        await draixon.send(embed=embed)
        await interaction.message.delete()


class SuggestionView(ui.View):
    @ui.button(emoji="๐๏ธ", label="Abbrechen", style=ButtonStyle.danger)
    async def cancel_bugreport(self, button, interaction: Interaction):
        await interaction.message.delete()

    @ui.button(emoji="๐ฌ", label="Vorschlag erstellen", style=ButtonStyle.success)
    async def report_bug(self, button, interaction):
        await interaction.response.send_modal(SuggestionModal(title="Vorschlag erstellen"))


# Wรผnsche
class WishModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Dein Username (Username#0000)", style=InputTextStyle.short))
        self.add_item(ui.InputText(
            label="Wunsch Titel", style=InputTextStyle.short))
        self.add_item(ui.InputText(
            label="Was ist dein Wunsch?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="๐ญ Neuer Wunsch ๐ญ")
        embed.add_field(
            name="Username", value=self.children[0].value, inline=False)
        embed.add_field(
            name="Wunsch Titel", value=self.children[1].value, inline=False)
        embed.add_field(
            name="Was ist dein Wunsch?", value=self.children[2].value, inline=False)

        draixon = await interaction.client.fetch_user(479537494384181248)

        await interaction.response.send_message(f"โ Wunsch wurde erfolgreich eingereicht. Vielen Dank โค๏ธ", ephemeral=True)
        await draixon.send(embed=embed)
        await interaction.message.delete()


class WishView(ui.View):
    @ui.button(emoji="๐๏ธ", label="Abbrechen", style=ButtonStyle.danger)
    async def cancel_bugreport(self, button, interaction: Interaction):
        await interaction.message.delete()

    @ui.button(emoji="๐ฌ", label="Wunsch erstellen", style=ButtonStyle.success)
    async def report_bug(self, button, interaction):
        await interaction.response.send_modal(WishModal(title="Wunsch erstellen"))
