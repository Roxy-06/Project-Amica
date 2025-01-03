import psutil
import tkinter as tk
from tkinter import ttk


class CPUMonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Monitor")
        self.root.geometry("500x500")
        self.root.configure(bg="black")

        # Header label
        self.header_label = tk.Label(
            root, text="CPU Usage Monitor", font=("Arial", 16, "bold"), fg="red", bg="black"
        )
        self.header_label.pack(pady=10)

        # Frame for CPU usage
        self.usage_frame = tk.Frame(root, bg="black")
        self.usage_frame.pack(fill="both", expand=True)

        # Overall CPU usage label
        self.overall_cpu_label = tk.Label(
            self.usage_frame, text="Overall CPU Usage: ", font=("Arial", 14), fg="red", bg="black"
        )
        self.overall_cpu_label.pack(anchor="w", padx=20, pady=5)

        # Per-core CPU usage labels
        self.core_labels = []
        for i in range(psutil.cpu_count()):
            core_label = tk.Label(
                self.usage_frame,
                text=f"Core {i + 1} Usage: ",
                font=("Arial", 12),
                fg="red",
                bg="black",
            )
            core_label.pack(anchor="w", padx=20)
            self.core_labels.append(core_label)

        # Start updating the information
        self.update_cpu_info()

    def update_cpu_info(self):
        # Update overall CPU usage
        overall_cpu = psutil.cpu_percent(interval=1)
        self.overall_cpu_label.config(text=f"Overall CPU Usage: {overall_cpu}%")

        # Update per-core CPU usage
        per_cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        for i, core_label in enumerate(self.core_labels):
            core_label.config(text=f"Core {i + 1} Usage: {per_cpu_usage[i]}%")

        # Schedule the next update
        self.root.after(1000, self.update_cpu_info)


if __name__ == "__main__":
    root = tk.Tk()
    app = CPUMonitorApp(root)
    root.mainloop()
