

class CpuMonitor:
    cpu_count = None
    usage_percent = None
    loadavg = None
    cpu_times = None

    def __init__(self, cpu_mon_data):
        self.cpu_count = cpu_mon_data.get('cpu_count')
        self.usage_percent = cpu_mon_data.get('usage_percent')
        self.loadavg = cpu_mon_data.get('loadavg', [])
        self.cpu_times = self.CpuTimes(cpu_mon_data.get('cpu_times'))

    class CpuTimes:
        user = None
        system = None
        idle = None

        def __init__(self, cpu_times_data):
            self.user = cpu_times_data.get('user')
            self.system = cpu_times_data.get('system')
            self.idle = cpu_times_data.get('idle')