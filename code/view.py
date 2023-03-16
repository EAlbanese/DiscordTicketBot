from discord import ui, ButtonStyle, InputTextStyle, Interaction, Embed, PermissionOverwrite, ChannelType, Client
import database as database
import datetime

client = Client()
db = database.Database("bot.db")


class variableManager(ui.View):
    threadID = 0

# Ticket System


class TicketManageView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ui.button(label="Ticket schliessen", style=ButtonStyle.primary)
    async def first_button_callback(self, button,  interaction: Interaction):
        ticketlogs = await interaction.guild.fetch_channel(1072160823088267314)

        ticketId = db.get_ticket_id_by_channel_id(
            interaction.message.channel.id)
        ticketinfo = db.get_ticket_info(ticketId)
        ticketClosedBy = interaction.guild.get_member(interaction.user.id)
        memberName = interaction.guild.get_member(ticketinfo[2])
        moderatorName = interaction.guild.get_member(ticketinfo[3])

        if ticketinfo[3] is None:
            await interaction.response.send_message("⛔ Keine Berechtigung!", ephemeral=True)
            return

        if ticketinfo[3] is interaction.user.id:
            await interaction.response.send_message("⛔ Das Ticket kann nur durch den claimer dieses Ticket geschlossen werden.", ephemeral=True)
            return

        embed = Embed(title=f"🔒 Ticket wurde geschlossen")
        embed.add_field(name="🎫 Ticket ID",
                        value=f'{ticketinfo[0]}', inline=False)
        embed.add_field(name="🎫 Channel ID",
                        value=f'{ticketinfo[1]}', inline=False)
        embed.add_field(name="👤 Ticket geöffnet von",
                        value=f'{memberName}', inline=False)
        embed.add_field(name="✅ Ticket geclaimt von",
                        value=f'{moderatorName}', inline=False)
        embed.add_field(name="🔒 Ticket geschlossen von",
                        value=f'{ticketClosedBy}', inline=False)

        await ticketlogs.send(embed=embed)
        await interaction.response.pong()
        await interaction.channel.delete()

    @ui.button(label="Claim Ticket", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction: Interaction):
        staffrole = interaction.guild.get_role(1070629289520807947)
        if staffrole not in interaction.user.roles:
            await interaction.response.send_message("⛔ Keine Berechtigung!", ephemeral=True)
            return
        embed = Embed(title="Ticket Status geändert: Wir sind dabei!",
                      description=f"<@{interaction.user.id}> kümmert sich um dein Ticket")
        embed.author.name = interaction.user.display_name
        embed.author.icon_url = interaction.user.display_avatar

        ticketId = db.get_ticket_id_by_channel_id(
            interaction.message.channel.id)
        ticketinfo = db.get_ticket_info(ticketId)
        db.update_claimed_ticket(interaction.user.id, ticketinfo[1])

        await interaction.response.send_message(embed=embed)


class SupportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Wo benötigst du Hilfe?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(
            title="Anliegen", description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(name="Wo benötigst du Hilfe?",
                        value=self.children[0].value)
        category = await interaction.guild.fetch_channel(1076894213083496509)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id,
                         round(create_date.timestamp()))
        count = db.get_ticket_id(round(create_date.timestamp()))

        staffrole = interaction.guild.get_role(1070629289520807947)
        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name} - {count}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            staffrole: PermissionOverwrite(read_messages=True)
        })

        db.update_ticket(ticketchannel.id, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@&{staffrole.id}>", embed=embed, view=TicketManageView())


class TeamComplaintModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Was für eine Team Beschwerde hast du?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Team Beschwerde",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(name="Was für eine Team Beschwerde hast du?",
                        value=self.children[0].value)
        category = await interaction.guild.fetch_channel(1076894213083496509)
        adminrole = interaction.guild.get_role(1071486720849223792)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, round(create_date.timestamp()))
        count = db.get_ticket_id(round(create_date.timestamp()))

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name} - {count}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })

        db.update_ticket(ticketchannel.id, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@&{adminrole.id}>", embed=embed, view=TicketManageView())


class BewerbungModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs, timeout=None)

        self.add_item(ui.InputText(
            label="Als was möchtest du dich bewerben?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Bewerbung",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(
            name="Als was möchtest du dich bewerben?", value=self.children[0].value)

        formembed = Embed(title="Bewerbung einreichen",
                          description="Wir bitten dich das folgenden Formular auszufüllen, damit unser Team sich deine Bewerbung anschauen kann.")
        formembed.add_field(
            name='Google Forms:', value='[Bewerbungs Formular](https://forms.gle/mt5sfLnahoHdm3pv6)')
        category = await interaction.guild.fetch_channel(1076894213083496509)
        adminrole = interaction.guild.get_role(1070629289520807947)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, round(create_date.timestamp()))
        count = db.get_ticket_id(round(create_date.timestamp()))

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name} - {count}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })

        db.update_ticket(ticketchannel.id, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@&{adminrole.id}>", embed=embed, view=TicketManageView())
        await ticketchannel.send(embed=formembed)


class SupportTicketCreateView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @ ui.button(emoji="🆘", label="Anliegen", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(SupportModal(title="Anliegen"))

    @ ui.button(emoji="📩", label="Team Beschwerde", style=ButtonStyle.danger)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_modal(TeamComplaintModal(title="Team Beschwerde"))

    @ ui.button(emoji="📝", label="Bewerbung", style=ButtonStyle.success)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_modal(BewerbungModal(title="Bewerbung"))


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
        embed = Embed(title="❗ Neuer Bug-Report ❗")
        embed.add_field(
            name="Username", value=self.children[0].value, inline=False)
        embed.add_field(
            name="Bug Titel", value=self.children[1].value, inline=False)
        embed.add_field(
            name="Beschreibe dein Vorgehen bis zum Bug", value=self.children[2].value, inline=False)
        embed.add_field(
            name="Wie oft ist das aufgetreten?", value=self.children[3].value, inline=False)

        draixon = await interaction.client.fetch_user(479537494384181248)

        await interaction.response.send_message(f"✅ Bug wurde erfolgreich gemeldet. Vielen Dank ❤️", ephemeral=True)
        await draixon.send(embed=embed)
        await interaction.message.delete()


class BugReportCreateView(ui.View):
    @ui.button(emoji="🗑️", label="Abbrechen", style=ButtonStyle.danger)
    async def cancel_bugreport(self, button, interaction: Interaction):
        await interaction.message.delete()

    @ui.button(emoji="📬", label="Bug melden", style=ButtonStyle.success)
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
        embed = Embed(title="🛠️ Neuer Verbesserungsvorschlag 🛠️")
        embed.add_field(
            name="Username", value=self.children[0].value, inline=False)
        embed.add_field(
            name="Verbesserungsvorschlag Titel", value=self.children[1].value, inline=False)
        embed.add_field(
            name="Was kann ich verbesser?", value=self.children[2].value, inline=False)

        draixon = await interaction.client.fetch_user(479537494384181248)

        await interaction.response.send_message(f"✅ Vorschlag wurde erfolgreich eingereicht. Vielen Dank ❤️", ephemeral=True)
        await draixon.send(embed=embed)
        await interaction.message.delete()


class SuggestionView(ui.View):
    @ui.button(emoji="🗑️", label="Abbrechen", style=ButtonStyle.danger)
    async def cancel_bugreport(self, button, interaction: Interaction):
        await interaction.message.delete()

    @ui.button(emoji="📬", label="Vorschlag erstellen", style=ButtonStyle.success)
    async def report_bug(self, button, interaction):
        await interaction.response.send_modal(SuggestionModal(title="Vorschlag erstellen"))


# Wünsche
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
        embed = Embed(title="💭 Neuer Wunsch 💭")
        embed.add_field(
            name="Username", value=self.children[0].value, inline=False)
        embed.add_field(
            name="Wunsch Titel", value=self.children[1].value, inline=False)
        embed.add_field(
            name="Was ist dein Wunsch?", value=self.children[2].value, inline=False)

        draixon = await interaction.client.fetch_user(479537494384181248)

        await interaction.response.send_message(f"✅ Wunsch wurde erfolgreich eingereicht. Vielen Dank ❤️", ephemeral=True)
        await draixon.send(embed=embed)
        await interaction.message.delete()


class WishView(ui.View):
    @ui.button(emoji="🗑️", label="Abbrechen", style=ButtonStyle.danger)
    async def cancel_bugreport(self, button, interaction: Interaction):
        await interaction.message.delete()

    @ui.button(emoji="📬", label="Wunsch erstellen", style=ButtonStyle.success)
    async def report_bug(self, button, interaction):
        await interaction.response.send_modal(WishModal(title="Wunsch erstellen"))
