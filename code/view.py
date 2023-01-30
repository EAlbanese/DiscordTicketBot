from discord import ui, ButtonStyle, InputTextStyle, Interaction, Embed, PermissionOverwrite


# Ticket System

class TicketManageView(ui.View):
    @ui.button(label="Ticket schliessen", style=ButtonStyle.primary)
    async def first_button_callback(self, button, interaction):
        await interaction.response.pong()
        await interaction.channel.delete()

    @ui.button(label="Claim Ticket", style=ButtonStyle.primary)
    async def second_button_callback(self, button, interaction):
        staffrole = interaction.guild.get_role(1069599130709659678)
        if staffrole not in interaction.user.roles:
            await interaction.response.send_message("⛔ Keine Berechtigung!", ephemeral=True)
            return
        embed = Embed(title="Ticket Status geändert: Wir sind dabei!",
                      description=f"<@{interaction.user.id}> kümmert sich um dein Ticket.")
        embed.author.name = interaction.user.display_name
        embed.author.icon_url = interaction.user.display_avatar
        await interaction.response.send_message(embed=embed)


# class ReportUserModal(ui.Modal):
#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)

#         self.add_item(ui.InputText(
#             label="Which user and why do you want to report him", style=InputTextStyle.long))

#     async def callback(self, interaction: Interaction):
#         embed = Embed(title="User Report",
#                       description="✅ Thank you for contacting support. Our team will take good care of your concern.")
#         embed.add_field(
#             name="Which user and why do you want to report him", value=self.children[0].value)

#         category = await interaction.guild.fetch_channel(1069598764966367313)
#         staffrole = interaction.guild.get_role(1069599130709659678)

#         ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
#             interaction.user: PermissionOverwrite(read_messages=True),
#             interaction.guild.default_role: PermissionOverwrite(
#                 read_messages=False),
#             staffrole: PermissionOverwrite(read_messages=True)
#         })
#         await interaction.response.send_message(f"Created ticket in <#{ticketchannel.id}>", ephemeral=True)
#         await ticketchannel.send(f"<@{interaction.user.id}> <@{staffrole.id}>", embed=embed, view=TicketManageView())


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
        category = await interaction.guild.fetch_channel(1069598764966367313)
        staffrole = interaction.guild.get_role(1069599130709659678)
        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            staffrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{staffrole.id}>", embed=embed, view=TicketManageView())


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
        category = await interaction.guild.fetch_channel(1069598764966367313)
        staffrole = interaction.guild.get_role(1069599130709659678)
        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            staffrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{staffrole.id}>", embed=embed, view=TicketManageView())


class ApplicationModal(ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(ui.InputText(
            label="Als was möchtest du dich bewerben?", style=InputTextStyle.long))

    async def callback(self, interaction: Interaction):
        embed = Embed(title="Application",
                      description="✅ Danke, dass du dich an den Support gewandt hast. Unser Team wird sich gut darum kümmern!")
        embed.add_field(
            name="Als was möchtest du dich bewerben?", value=self.children[0].value)

        category = await interaction.guild.fetch_channel(1069598764966367313)
        adminrole = interaction.guild.get_role(1069599130709659678)

        ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
            interaction.user: PermissionOverwrite(read_messages=True),
            interaction.guild.default_role: PermissionOverwrite(
                read_messages=False),
            adminrole: PermissionOverwrite(read_messages=True)
        })
        await interaction.response.send_message(f"Ticket eröffnet in <#{ticketchannel.id}>", ephemeral=True)
        await ticketchannel.send(f"<@{interaction.user.id}> <@{adminrole.id}>", embed=embed, view=TicketManageView())


# class StaffComplaintModal(ui.Modal):

#     def __init__(self, *args, **kwargs) -> None:
#         super().__init__(*args, **kwargs)

#         self.add_item(ui.InputText(
#             label="Who from team do you want to report?", style=InputTextStyle.long))

#     async def callback(self, interaction: Interaction):
#         embed = Embed(title="Staff complaint",
#                       description="✅ Thank you for creating a ticket and reporting someone on staff. We are sorry and our admins will do the best they can. ")
#         embed.add_field(
#             name="Who from team do you want to report?", value=self.children[0].value)

#         category = await interaction.guild.fetch_channel(1069598764966367313)
#         adminrole = interaction.guild.get_role(1069599130709659678)

#         ticketchannel = await interaction.guild.create_text_channel(f"{interaction.user.display_name}", category=category, overwrites={
#             interaction.user: PermissionOverwrite(read_messages=True),
#             interaction.guild.default_role: PermissionOverwrite(
#                 read_messages=False),
#             adminrole: PermissionOverwrite(read_messages=True)
#         })
#         await interaction.response.send_message(f"Created ticket in <#{ticketchannel.id}>", ephemeral=True)
#         await ticketchannel.send(f"<@{interaction.user.id}> <@{adminrole.id}>", embed=embed, view=TicketManageView())


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


# class AddminTicketCreatView(ui.View):
#     @ ui.button(emoji="📝", label="Application", style=ButtonStyle.primary)
#     async def first_button_callback(self, button, interaction):
#         await interaction.response.send_modal(ReportUserModal(title="Application"))

#     @ ui.button(emoji="⛔", label="Team complaint", style=ButtonStyle.primary)
#     async def third_button_callback(self, button, interaction):
#         await interaction.response.send_modal(BotProblemsModal(title="Team complaint"))
