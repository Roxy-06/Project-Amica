import requests
import re
import socket
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import messagebox

def is_https(url):
    """Check if the URL uses HTTPS."""
    return url.startswith("https://")

def is_valid_url(url):
    """Check if the URL format is valid using a regular expression."""
    regex = re.compile(
        r'^(?:http|ftp)s?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}|'  # IPv4
        r'\[?[A-F0-9]*:[A-F0-9:]+\]?)'  # IPv6
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    return re.match(regex, url) is not None

def is_domain_reachable(url):
    """Check if the domain of the URL is reachable via DNS lookup."""
    try:
        domain = re.findall(r'://([^/]+)', url)[0]  # Extract the domain
        socket.gethostbyname(domain)
        return True
    except Exception:
        return False

def is_blacklisted(url):
    """Check if the URL contains blacklisted keywords or domains."""
    blacklisted_keywords = ["malicious", "phishing", "unsafe", "fraud"]
    return any(keyword in url.lower() for keyword in blacklisted_keywords)

def has_suspicious_keywords(url):
    """Check for suspicious keywords that might indicate phishing."""
    suspicious_keywords = ["login", "verify", "secure", "account"]
    return any(keyword in url.lower() for keyword in suspicious_keywords)

def is_url_too_long(url):
    """Check if the URL length exceeds a suspicious threshold."""
    return len(url) > 100  # Example threshold

def uses_ip_address(url):
    """Check if the URL uses an IP address instead of a domain."""
    return re.match(r'http[s]?://\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', url) is not None

def check_url_safety(url):
    """Perform a comprehensive safety check on the URL."""
    if not is_valid_url(url):
        return "Invalid URL format.", None, None

    safe_count = 0
    unsafe_count = 0

    # HTTPS check
    if is_https(url):
        safe_count += 1
    else:
        unsafe_count += 1

    # Domain reachability
    if is_domain_reachable(url):
        safe_count += 1
    else:
        unsafe_count += 1

    # Blacklist check
    if is_blacklisted(url):
        unsafe_count += 1

    # Suspicious keywords
    if has_suspicious_keywords(url):
        unsafe_count += 1

    # URL length check
    if is_url_too_long(url):
        unsafe_count += 1

    # IP address check
    if uses_ip_address(url):
        unsafe_count += 1

    return None, safe_count, unsafe_count

def plot_results(safe_count, unsafe_count):
    """Visualize safety results as a pie chart."""
    labels = ['Safe', 'Unsafe']
    sizes = [safe_count, unsafe_count]
    colors = ['#4CAF50', '#F44336']
    explode = (0.1, 0)  # explode the 1st slice (Safe)

    plt.figure(figsize=(8, 6))
    plt.pie(sizes, explode=explode, labels=labels, colors=colors,
            autopct='%1.1f%%', shadow=True, startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('URL Safety Check')
    plt.show()

def handle_check_url():
    url = entry.get()  # Get the URL from the entry widget
    error_message, safe_count, unsafe_count = check_url_safety(url)
    
    if error_message:
        messagebox.showerror("Error", error_message)
        return
    
    total_count = safe_count + unsafe_count
    if total_count > 0:
        safe_percentage = (safe_count / total_count) * 100
        result_text.set(f"Safe Count: {safe_count}, Unsafe Count: {unsafe_count}\n"
                        f"Safe Percentage: {safe_percentage:.2f}%")
        
        if safe_percentage >= 70:
            messagebox.showinfo("Result", "The URL is considered safe.")
        else:
            messagebox.showwarning("Result", "The URL is considered unsafe.")
    else:
        messagebox.showinfo("Result", "No checks were performed.")

def handle_plot():
    url = entry.get()  # Get the URL from the entry widget
    _, safe_count, unsafe_count = check_url_safety(url)
    if safe_count is not None and unsafe_count is not None:
        plot_results(safe_count, unsafe_count)

# Create the Tkinter window
root = tk.Tk()
root.title("URL Security Checker")

# Entry widget for URL input
tk.Label(root, text="Enter URL:").pack(pady=5)
entry = tk.Entry(root, width=50)
entry.pack(pady=5)

# Result display
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, fg="blue", wraplength=400, justify="left")
result_label.pack(pady=10)

# Buttons
check_button = tk.Button(root, text="Check URL", command=handle_check_url)
check_button.pack(pady=5)

plot_button = tk.Button(root, text="Plot Results", command=handle_plot)
plot_button.pack(pady=5)

# Run the Tkinter main loop
root.mainloop()
