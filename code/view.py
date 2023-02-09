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

        threadId = db.get_ticket_thread_id()
        thread = interaction.guild.get_thread(threadId)

        ticketId = db.get_ticket_id(threadId)
        ticketinfo = db.get_ticket_info(ticketId)
        ticketClosedBy = interaction.user.display_name
        memberName = interaction.guild.get_member(ticketinfo[2])
        moderatorName = interaction.guild.get_member(ticketinfo[3])

        embed = Embed(title=f"🔒 Ticket wurde geschlossen")
        embed.add_field(name="🎫 Ticket ID",
                        value=f'{ticketinfo[0]} \n\n **🎫 Thread ID** \n {ticketinfo[1]} \n\n **👤 Ticket geöffnet von** \n {memberName} \n\n **✅ Ticket geclaimt von** \n {moderatorName} \n\n **🔒 Ticket geschlossen von** \n {ticketClosedBy}')

        await channel.send(embed=embed, view=TicketLogsView())
        await thread.edit(archived=True, locked=True)
        await interaction.response.defer()

    @ui.button(label="Claim Ticket", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction: Interaction):
        staffrole = interaction.guild.get_role(1070629289520807947)

        thread = interaction.guild.get_thread(variableManager.threadID)
        count = db.get_ticket_id(variableManager.threadID)

        if staffrole not in interaction.user.roles:
            await interaction.response.send_message("⛔ Keine Berechtigung!", ephemeral=True)
            return
        db.update_claimed_ticket(interaction.user.id, count)
        embed = Embed(title="Ticket Status geändert: Wir sind dabei!",
                      description=f"<@{interaction.user.id}> kümmert sich um dein Ticket.")
        embed.author.name = interaction.user.display_name
        embed.author.icon_url = interaction.user.display_avatar
        await interaction.response.send_message(embed=embed)
        await thread.edit(name=f"{count} - {interaction.user.name}")


class TicketLogsView(ui.View):
    @ui.button(label="🔓 Ticket erneut öffnen", style=ButtonStyle.primary)
    async def reopenTicket(self, button,  interaction: Interaction):
        threadId = db.get_ticket_thread_id()
        thread = interaction.guild.get_thread(threadId)

        await thread.edit(archived=False, locked=False)
        await interaction.response.send_message(f"<#{thread.id}> Ticket wurde wieder geöffnet", ephemeral=True)


class SupportModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Wo benötigst du Hilfe?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(
            title="Anliegen", description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(name="Wo benötigst du Hilfe?",
                        value=self.children[0].value)
        channel = await interaction.guild.fetch_channel(1071005969359847464)

        create_date = datetime.datetime.now()
        print(create_date)
        db.create_ticket(interaction.user.id, create_date)

        count = db.get_ticket_id(int(create_date.timestamp()))

        response = await channel.create_thread(name=f"{count} - {interaction.user.display_name}", type=ChannelType.private_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)

        db.update_ticket(variableManager.threadID, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@&{1070629289520807947}>", embed=embed, view=TicketManageView())


class TeamComplaintModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Was für eine Team Beschwerde hast du?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Team Beschwerde",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(name="Was für eine Team Beschwerde hast du?",
                        value=self.children[0].value)
        channel = await interaction.guild.fetch_channel(1071005969359847464)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, create_date)

        count = db.get_ticket_id(create_date)

        response = await channel.create_thread(name=f"{count} - {interaction.user.display_name}", type=ChannelType.private_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)

        db.update_ticket(variableManager.threadID, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@&{1071486720849223792}>", embed=embed, view=TicketManageView())


class ApplicationModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Als was möchtest du dich bewerben?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Bewerbung",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(
            name="Als was möchtest du dich bewerben?", value=self.children[0].value)

        channel = await interaction.guild.fetch_channel(1071005969359847464)

        create_date = datetime.datetime.now()
        db.create_ticket(interaction.user.id, create_date)

        count = db.get_ticket_id(create_date)

        response = await channel.create_thread(name=f"{count} - {interaction.user.display_name}", type=ChannelType.private_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)

        db.update_ticket(variableManager.threadID, count)

        await interaction.response.send_message(f"Ticket eröffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@&{1070629289520807947}>", embed=embed, view=TicketManageView())


class SupportTicketCreateView(ui.View):
    @ ui.button(emoji="📩", label="Anliegen", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(SupportModal(title="Anliegen Ticket"))

    @ ui.button(emoji="📩", label="Team Beschwerde", style=ButtonStyle.danger)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_modal(TeamComplaintModal(title="Team Beschwerde"))

    @ ui.button(emoji="📩", label="Bewerbung", style=ButtonStyle.success)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_modal(ApplicationModal(title="Bewerbung"))
