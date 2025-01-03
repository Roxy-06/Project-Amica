import time
from plyer import notification

def timer(seconds):
    print(f"Timer set for {seconds} seconds.")
    time.sleep(seconds)
    print("Time's up!")
    notification.notify(
        title="Timer Alert",
        message="Your timer has run out!",
        app_name="Timer App",
        timeout=10  # Notification will stay for 10 seconds
    )

def alarm(hour, minute):
    print(f"Alarm set for {hour:02d}:{minute:02d}.")
    while True:
        current_time = time.localtime()
        if current_time.tm_hour == hour and current_time.tm_min == minute:
            print("Alarm ringing!")
            notification.notify(
                title="Alarm Alert",
                message="Your alarm is ringing!",
                app_name="Alarm App",
                timeout=10  # Notification will stay for 10 seconds
            )
            break
        time.sleep(30)  # Check every 30 seconds

if __name__ == "__main__":
    choice = input("Do you want to set a timer or an alarm? (Enter 'timer' or 'alarm'): ").strip().lower()
    
    if choice == 'timer':
        try:
            seconds = int(input("Enter the time in seconds for the timer: "))
            timer(seconds)
        except ValueError:
            print("Please enter a valid integer.")
    
    elif choice == 'alarm':
        try:
            hour = int(input("Enter the hour for the alarm (0-23): "))
            minute = int(input("Enter the minute for the alarm (0-59): "))
            if 0 <= hour < 24 and 0 <= minute < 60:
                alarm(hour, minute)
            else:
                print("Please enter a valid time.")
        except ValueError:
            print("Please enter valid integers for hour and minute.")
    
    else:
        print("Invalid choice. Please enter 'timer' or 'alarm'.")