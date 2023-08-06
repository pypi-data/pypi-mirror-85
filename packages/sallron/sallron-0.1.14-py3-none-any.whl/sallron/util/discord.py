from sallron.util import settings, system
from discord_logger import DiscordLogger
from os import environ

def send_message(message, level="error", title="Exception raised", description="", metadata={}):
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
    metadata = system.system_stats()
    options = {
        "application_name": "Sallron",
        "service_name": f"{settings.INTERFACE_NAME}",
        "service_environment": "Production",
        "default_level": "info",
    }

    # logger = DiscordLogger(webhook_url=settings.DISCORD_WEBHOOK, **options)
    logger = DiscordLogger(webhook_url="https://discord.com/api/webhooks/770328180275806238/kd4bFFbNW-c3ol9cv4tbKXtsbOlCgW3n7RqYW9gjkuCr9c2ykcQyAcEdhM1ZfpiJ4IkN", **options)

    if level == 'error':
        logger.construct(
            title=f"{title}",
            level=f"{level}",
            description=f"{description}",
            error=message,
            metadata=metadata,
        )
    else:
        logger.construct(
            title=f"{title}",
            level=f"{level}",
            description=f"{description} \n {message}",
            metadata=metadata,
        )

    response = logger.send()

    pass