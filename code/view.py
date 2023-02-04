from discord import ui, ButtonStyle, InputTextStyle, Interaction, Embed, PermissionOverwrite, ChannelType, Client
import database as database

client = Client()
db = database.Database("bot.db")

class variableManager(ui.View):
    threadID = 0
    ticketCount = 0
    
# Ticket System

class TicketManageView(ui.View):
    @ui.button(label="Ticket schliessen", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.pong()
        await interaction.channel.delete()

    @ui.button(label="Claim Ticket", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction: Interaction):
        staffrole = interaction.guild.get_role(1070629289520807947)
        
        thread = interaction.guild.get_thread(variableManager.threadID)
        count = db.get_ticket_count()
               
        if staffrole not in interaction.user.roles:
            await interaction.response.send_message("⛔ Keine Berechtigung!", ephemeral=True)
            return
        embed = Embed(title="Ticket Status geändert: Wir sind dabei!",
                      description=f"<@{interaction.user.id}> kümmert sich um dein Ticket.")
        embed.author.name = interaction.user.display_name
        embed.author.icon_url = interaction.user.display_avatar
        await interaction.response.send_message(embed=embed)
        await thread.edit(name=f"{count[0]} - {interaction.user.name}")

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
        staffrole = interaction.guild.get_role(1070629289520807947)
        channel = await interaction.guild.fetch_channel(1071005969359847464)

        variableManager.ticketCount += 1
        ticket_count = variableManager.ticketCount
        db.update_ticket_count(ticket_count)
        count = db.get_ticket_count()

        response = await channel.create_thread(name=f"{count[0]} - {interaction.user.display_name}", type=ChannelType.private_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)

        await interaction.response.send_message(f"Ticket eröffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@{staffrole.id}>", embed=embed, view=TicketManageView())


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
        staffrole = interaction.guild.get_role(1070629289520807947)
        channel = await interaction.guild.fetch_channel(1071005969359847464)
        
        variableManager.ticketCount += 1
        ticket_count = variableManager.ticketCount
        db.update_ticket_count(ticket_count)
        count = db.get_ticket_count()

        response = await channel.create_thread(name=f"{count[0]} - {interaction.user.display_name}", type=ChannelType.public_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)
        
        await interaction.response.send_message(f"Ticket eröffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@{staffrole.id}>", embed=embed, view=TicketManageView())


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

        staffrole = interaction.guild.get_role(1070629289520807947)
        channel = await interaction.guild.fetch_channel(1071005969359847464)
        
        variableManager.ticketCount += 1
        ticket_count = variableManager.ticketCount
        db.update_ticket_count(ticket_count)
        count = db.get_ticket_count()

        response = await channel.create_thread(name=f"{count[0]} - {interaction.user.display_name}", type=ChannelType.public_thread)
        variableManager.threadID = response.id
        thread = interaction.guild.get_thread(variableManager.threadID)
        
        await interaction.response.send_message(f"Ticket eröffnet in <#{variableManager.threadID}>", ephemeral=True)
        await thread.send(f"<@{interaction.user.id}> <@{staffrole.id}>", embed=embed, view=TicketManageView())


class SupportTicketCreateView(ui.View):
    @ ui.button(emoji="📩", label="Anliegen", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.send_modal(SupportModal(title="Anliegen Ticket"))

    @ ui.button(emoji="📩", label="Team Beschwerde", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        await interaction.response.send_modal(TeamComplaintModal(title="Team Beschwerde"))

    @ ui.button(emoji="📩", label="Bewerbung", style=ButtonStyle.primary)
    async def third_button_callback(self, button, interaction):
        await interaction.response.send_modal(ApplicationModal(title="Bewerbung"))

