from sallron.util import s3, logger, discord, settings
import schedule
import datetime
import pytz
import sys

def send_to_s3_and_kill(log_dir):
    """
    Utility function to send the log to s3 and kill the process

    Args:
        log_dir (str): Directory containing log to be sent
    """
    masterlog_path = logger.get_logname(log_dir, 'master')
    errorslog_path = logger.get_logname(log_dir, 'errors')

    discord.send_message(
        message = f'Bucket hit: {settings.LOGGIN_BUCKET}',
        level = 'default',
        title = 'Logs backed up to S3 bucket',
        description = f'Files sent: \n{masterlog_path}\n{errorslog_path}'
    )

    s3.send_to_s3([masterlog_path, errorslog_path])

    sys.exit("Exiting from process after send log to S3.")

def schedule_log_sending_and_kill_process(log_dir, timezone):
    """
    Utility function to schedule the sending of log file to S3 and kill the hole process
    Args:
        obj_path (str): Path to object to be sent
        timezone (str): Timezone string supported by pytz
    """

    schedule.every().day.at(
        datetime.time(hour=0, minute=1, tzinfo=pytz.timezone(timezone)).strftime("%H:%M")
    ).do(send_to_s3_and_kill, log_dir=log_dir)