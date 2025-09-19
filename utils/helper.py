def category_helios(interaction):
    """
    Returns True if the command is used in a channel under the 'Helios Labs' category.
    Otherwise returns False.
    """
    category = getattr(interaction.channel, 'category', None)
    return category and category.name == "Helios Labs"

def require_helios_category(func):
    """
    Decorator for Discord commands to restrict usage to 'Helios Labs' category.
    Sends an ephemeral message and returns if used elsewhere.
    Usage: @require_helios_category above async command methods.
    """
    import functools
    @functools.wraps(func)
    async def wrapper(self, interaction, *args, **kwargs):
        if not category_helios(interaction):
            await interaction.response.send_message(
                "This command can only be used in the 'Helios Labs' category.", ephemeral=True)
            return
        return await func(self, interaction, *args, **kwargs)
    return wrapper
