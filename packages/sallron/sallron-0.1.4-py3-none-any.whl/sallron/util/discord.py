from discord_logger import DiscordLogger
from os import environ

def send_message_discord(message, metadata={}, interface_name="ga", level="error", title="Exception raised", description=" "):
    """
    Sends a message to a discord channel.

    Args:
        message (string): the message to be sent.
        metadata (dictionary): Any dictionary with information.
        interface_name (string): The name of the interface
        level (string): The level of the information being sent. Default is "error". Possibilities: error, warn, info, verbose, debug, success.
        title (string): Title of the message.
        description (string): Description of the message.
    """    

    options = {
        "application_name": "Raptor",
        "service_name": f"{interface_name}",
        "service_environment": "Production",
        "default_level": "info",
    }

    logger = DiscordLogger(webhook_url=environ.get('DISCORD_WEBHOOK'), **options)
    logger.construct(
        title=f"{title}",
        level=f"{level}",
        description=f"{description}",
        error=message,
        metadata=metadata,
    )

    response = logger.send()

    pass