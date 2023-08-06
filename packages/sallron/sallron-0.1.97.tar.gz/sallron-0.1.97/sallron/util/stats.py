from sallron.util import settings
from datetime import datetime
import psutil
import os

def program_settings():
    pid = os.getpid()
    return {
        'Timestamp' : str(datetime.now()),
        'OS' : settings.OS,
        'Interface' : settings.INTERFACE_NAME,
        'Timezone' : settings.TIMEZONE,
        'AWSRegion' : settings.AWS_REGION,
        'PID' : pid,
        'SID' : os.getsid(pid)
    }

def system_stats():
    uname_result = os.uname()
    return {
            'CPUt' : dict(psutil.cpu_times()._asdict()),
            'CPU%' : psutil.cpu_percent(),
            'VMem%' : dict(psutil.virtual_memory()._asdict()).get('percent'),
            'SMem%' : dict(psutil.swap_memory()._asdict()).get('percent'),
            'Disk%' : dict(psutil.disk_usage('/')._asdict()).get('percent'),
            'Sysname' : uname_result.sysname,
            'Nodename' : uname_result.nodename,
            'Sysrelease' : uname_result.release,
            'Sysversion' : uname_result.version.split(' ')[-1],
            'Sysmachine' : uname_result.machine
    }

def metadata_dict():
    return {**program_settings(), **system_stats()}
