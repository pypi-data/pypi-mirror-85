from sallron.util import s3
import schedule
import datetime
import pytz
import sys

def _send_to_s3_and_kill(log_dir):
    """
    Utility function to send the log to s3 and kill the process

    Args:
        log_dir (str): Directory containing log to be sent
    """

    s3.send_to_s3(log_dir)

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
    ).do(_send_to_s3_and_kill, log_dir=log_dir)