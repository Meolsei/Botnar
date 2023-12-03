import discord
from discord import app_commands
from discord.ext import commands

from dateutil.relativedelta import relativedelta
from datetime import date

class Util(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="age")
    async def age(self, interaction:discord.Interaction, 
                  year: app_commands.Range[int, 1900, 2023], 
                  month: app_commands.Range[int, 1, 12],
                  day: app_commands.Range[int, 1, 31]) -> None:
        """Input your age to check eligibility for the 18+ role."""

        async def calculate(birth):
            today = date.today()
            age2 = relativedelta(today, birth)
            return age2.years

        birth = date(year, month, day)
        age2 = await calculate(birth)
        
        role = interaction.guild.get_role(807955779113451522)
        logchannel = interaction.guild.get_channel(1126331517405237290)

        await interaction.response.send_message(f"You have indicated that you were born {age2} years ago.", ephemeral=True)
        await logchannel.send(f"{interaction.user.mention} indicated that they are {age2} years old.")

        if age2 >= 18:
            if role in interaction.user.roles:
                await interaction.followup.send(f"You already have the role.", ephemeral=True)
            else:
                await interaction.followup.send(f"You now have the role.", ephemeral=True)
                await interaction.user.add_roles(role)
        elif age2 <13:
                await interaction.followup.send(f"You have indicated that you are either 13 or below, this has been logged.", ephemeral=True)
        else:
                await interaction.followup.send(f"You are not eligible for the role.", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Util(bot))