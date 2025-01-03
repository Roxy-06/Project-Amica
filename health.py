import tkinter as tk
import psutil
import platform

def update_info():
    """Function to gather and update system information."""
    info_text = ""

    # System Information
    uname = platform.uname()
    info_text += "==== System Information ====\n"
    info_text += f"System: {uname.system}\n"
    info_text += f"Node Name: {uname.node}\n"
    info_text += f"Release: {uname.release}\n"
    info_text += f"Version: {uname.version}\n"
    info_text += f"Machine: {uname.machine}\n"
    info_text += f"Processor: {uname.processor}\n\n"

    # CPU Usage
    info_text += "==== CPU Usage ====\n"
    info_text += f"CPU Usage: {psutil.cpu_percent(interval=1)}%\n"
    info_text += f"CPU Frequency: {psutil.cpu_freq().current:.2f} MHz\n"
    info_text += f"CPU Cores: {psutil.cpu_count(logical=False)} Physical, {psutil.cpu_count(logical=True)} Logical\n\n"

    # Memory Status
    virtual_mem = psutil.virtual_memory()
    info_text += "==== Memory Status ====\n"
    info_text += f"Total RAM: {virtual_mem.total / (1024 ** 3):.2f} GB\n"
    info_text += f"Available RAM: {virtual_mem.available / (1024 ** 3):.2f} GB\n"
    info_text += f"Used RAM: {virtual_mem.used / (1024 ** 3):.2f} GB ({virtual_mem.percent}%)\n\n"

    disk_usage = psutil.disk_usage('/')
    info_text += f"Total Storage (ROM): {disk_usage.total / (1024 ** 3):.2f} GB\n"
    info_text += f"Used Storage: {disk_usage.used / (1024 ** 3):.2f} GB ({disk_usage.percent}%)\n"
    info_text += f"Free Storage: {disk_usage.free / (1024 ** 3):.2f} GB\n\n"

    # Battery Status
    if hasattr(psutil, "sensors_battery"):
        battery = psutil.sensors_battery()
        info_text += "==== Battery Status ====\n"
        if battery:
            info_text += f"Battery Percentage: {battery.percent}%\n"
            info_text += f"Power Plugged In: {'Yes' if battery.power_plugged else 'No'}\n"
            info_text += f"Time Left: {battery.secsleft // 60 if battery.secsleft != psutil.POWER_TIME_UNLIMITED else 'Unlimited'} minutes\n\n"
        else:
            info_text += "No battery detected.\n\n"
    else:
        info_text += "Battery feature not supported on this system.\n\n"

    # Running Processes
    info_text += "==== Running Processes ====\n"
    processes = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            processes.append(proc.info)
        except psutil.NoSuchProcess:
            pass
    processes = sorted(processes, key=lambda p: p['cpu_percent'], reverse=True)[:10]
    for proc in processes:
        info_text += f"PID: {proc['pid']}, Name: {proc['name']}, CPU: {proc['cpu_percent']}%, Memory: {proc['memory_percent']:.2f}%\n"

    # Update text in the GUI
    text_widget.config(state=tk.NORMAL)
    text_widget.delete(1.0, tk.END)
    text_widget.insert(tk.END, info_text)
    text_widget.config(state=tk.DISABLED)

    # Update the information every 5 seconds
    root.after(5000, update_info)


# Create the main tkinter window
root = tk.Tk()
root.title("System Monitor")
root.geometry("800x600")
root.configure(bg="black")

# Create a Text widget to display the information
text_widget = tk.Text(root, bg="black", fg="red", font=("Consolas", 12), wrap=tk.WORD)
text_widget.pack(expand=True, fill=tk.BOTH)
text_widget.config(state=tk.DISABLED)

# Start updating the information
update_info()

# Run the tkinter main loop
root.mainloop()
