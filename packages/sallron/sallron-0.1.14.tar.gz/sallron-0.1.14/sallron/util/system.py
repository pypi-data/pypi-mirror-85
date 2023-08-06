import psutil

def system_stats():
    return {
            'CPUt' : dict(psutil.cpu_times()._asdict()),
            'CPU%' : psutil.cpu_percent(),
            'VMem%' : dict(psutil.virtual_memory()._asdict()).get('percent'),
            'SMem%' : dict(psutil.swap_memory()._asdict()).get('percent'),
            'Disk%' : dict(psutil.disk_usage('/')._asdict()).get('percent')
            }