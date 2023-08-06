from sallron.util import settings, stats
from discord_logger import DiscordLogger

def send_message(message, level="error", title="Exception raised", description=""):
    """
    Sends a message to a discord channel.

    Args:
        message (string): the message to be sent.
        interface_name (string): The name of the interface
        level (string): The level of the information being sent. Default is "error". Possibilities: error, warn, info, verbose, debug, success.
        title (string): Title of the message.
        description (string): Description of the message.
    """
    webhook_url = settings.DISCORD_WEBHOOK
    metadata = stats.metadata_dict()
    options = {
        "application_name": "Sallron",
        "service_name": f"{settings.INTERFACE_NAME}",
        "service_environment": "Production",
        "default_level": "info",
    }

    logger = DiscordLogger(webhook_url=webhook_url, **options)

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
            description=f"{description}\n{message}",
            metadata=metadata,
        )

    response = logger.send()

    pass