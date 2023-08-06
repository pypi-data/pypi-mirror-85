from discord_logger import DiscordLogger
from sallron.util import settings

def send_message(message, level="error", title="Exception raised", description="", metadata={}):
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

    options = {
        "application_name": "Sallron",
        "service_name": f"{settings.INTERFACE_NAME}",
        "service_environment": "Production",
        "default_level": "info",
    }

    logger = DiscordLogger(webhook_url=webhook_url, **options)

    try:
        from sallron.util import stats
        metadata = stats.metadata_dict()
    except:
        metadata = metadata
        metadata["sallronStatus"] = "Sallron could not import psutil"

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