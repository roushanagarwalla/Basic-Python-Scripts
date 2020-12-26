import platform
from datetime import datetime
import psutil
import os
from rich import console, print

console = console.Console()

console.print("[yellow]\nBasic System Information\n[/yellow]", justify="center")

print("[+] Architecture :", platform.architecture()[0])
print("[+] Machine :", platform.machine())
print("[+] Operating System Release :", platform.release())
print("[+] System Name :",platform.system())
print("[+] Operating System Version :", platform.version())
print("[+] Node: " + platform.node())
print("[+] Platform :", platform.platform())
print("[+] Processor :",platform.processor())

boot_time = datetime.fromtimestamp(psutil.boot_time())
print("[+] System Boot Time :", boot_time)

with open("/proc/uptime", "r") as f:
    uptime = f.read().split(" ")[0].strip()
uptime = int(float(uptime))
uptime_hours = uptime // 3600
uptime_minutes = (uptime % 3600) // 60
print("[+] System Uptime : " + str(uptime_hours) + ":" + str(uptime_minutes) + " hours")

pids = []
for subdir in os.listdir('/proc'):
    if subdir.isdigit():
        pids.append(subdir)
print('[+] Total number of processes : {0}'.format(len(pids)))


console.print("[yellow]\nCPU Information\n[/yellow]", justify="center")

print("[+] Number of Physical cores :", psutil.cpu_count(logical=False))
print("[+] Number of Total cores :", psutil.cpu_count(logical=True))
print("\n")

cpu_frequency = psutil.cpu_freq()
print(f"[+] Max Frequency : {cpu_frequency.max:.2f}Mhz")
print(f"[+] Min Frequency : {cpu_frequency.min:.2f}Mhz")
print(f"[+] Current Frequency : {cpu_frequency.current:.2f}Mhz")
print("\n")

for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"[+] CPU Usage of Core {i} : {percentage}%")
print(f"[+] Total CPU Usage : {psutil.cpu_percent()}%")


with open("/proc/cpuinfo", "r")  as f:
    file_info = f.readlines()

cpuinfo = [x.strip().split(":")[1] for x in file_info if "model name"  in x]
for index, item in enumerate(cpuinfo):
    print("[+] Processor " + str(index) + " : " + item)

def bytes_to_GB(bytes):
    gb = bytes/(1024*1024*1024)
    gb = round(gb, 2)
    return gb

virtual_memory = psutil.virtual_memory()
console.print("[yellow]\nMemory Information\n[/yellow]", justify="center")

print("[+] Total Memory present :", bytes_to_GB(virtual_memory.total), "Gb")
print("[+] Total Memory Available :", bytes_to_GB(virtual_memory.available), "Gb")
print("[+] Total Memory Used :", bytes_to_GB(virtual_memory.used), "Gb")
print("[+] Percentage Used :", virtual_memory.percent, "%")
print("\n")

swap = psutil.swap_memory()
print(f"[+] Total swap memory :{bytes_to_GB(swap.total)}")
print(f"[+] Free swap memory : {bytes_to_GB(swap.free)}")
print(f"[+] Used swap memory : {bytes_to_GB(swap.used)}")
print(f"[+] Percentage Used: {swap.percent}%")

print("\nReading the /proc/meminfo file: \n")

with open("/proc/meminfo", "r") as f:
    lines = f.readlines()

print("[+] " + lines[0].strip())
print("[+] " + lines[1].strip())

disk_partitions = psutil.disk_partitions()
console.print("[yellow]\nDisk Information\n[/yellow]", justify="center")

for partition in disk_partitions:
    print("[+] Partition Device : ", partition.device)
    print("[+] File System : ", partition.fstype)
    print("[+] Mountpoint : ", partition.mountpoint)

    disk_usage = psutil.disk_usage(partition.mountpoint)
    print("[+] Total Disk Space :", bytes_to_GB(disk_usage.total), "GB")
    print("[+] Free Disk Space :", bytes_to_GB(disk_usage.free), "GB")
    print("[+] Used Disk Space :", bytes_to_GB(disk_usage.used), "GB")
    print("[+] Percentage Used :", disk_usage.percent, "%")

disk_rw = psutil.disk_io_counters()
print(f"[+] Total Read since boot : {bytes_to_GB(disk_rw.read_bytes)} GB")
print(f"[+] Total Write sice boot : {bytes_to_GB(disk_rw.write_bytes)} GB")

if_addrs = psutil.net_if_addrs()
console.print("[yellow]\nNetwork Information\n[/yellow]", justify="center")

for interface_name, interface_addresses in if_addrs.items():
    for address in interface_addresses:
        print(f"Interface :", interface_name)
        if str(address.family) == 'AddressFamily.AF_INET':
            print("[+] IP Address :", address.address)
            print("[+] Netmask :", address.netmask)
            print("[+] Broadcast IP :", address.broadcast)
        elif str(address.family) == 'AddressFamily.AF_PACKET':
            print("[+] MAC Address :", address.address)
            print("[+] Netmask :", address.netmask)
            print("[+] Broadcast MAC :",address.broadcast)

net_io = psutil.net_io_counters()
print("[+] Total Bytes Sent :", bytes_to_GB(net_io.bytes_sent))
print("[+] Total Bytes Received :", bytes_to_GB(net_io.bytes_recv))

battery = psutil.sensors_battery()
console.print("[yellow]\nBattery Information\n[/yellow]", justify="center")
print("[+] Battery Percentage :", round(battery.percent, 1), "%")
print("[+] Battery time left :", round(battery.secsleft/3600, 2), "hr")
print("[+] Power Plugged :", battery.power_plugged)