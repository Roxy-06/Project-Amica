import socket

def get_system_name():
    # Get the hostname of the machine
    hostname = socket.gethostname()
    return hostname

if __name__ == "__main__":
    system_name = get_system_name()
    print(f"System Name: {system_name}")