import os
import psutil
import win32gui
import win32process
import time
from datetime import datetime, timedelta

# Define the custom folder in the C drive
custom_folder = r"C:\WindowsX86"
log_file = os.path.join(custom_folder, "app_usage.log")
log_buffer = []

# Ensure the custom folder exists
if not os.path.exists(custom_folder):
    os.makedirs(custom_folder)

def safe_write_log(message):
    with open(log_file, 'a', encoding='utf-8') as log_file_handle:
        log_file_handle.write(message + "\n")

def flush_log_buffer():
    with open(log_file, 'a', encoding='utf-8') as log_file_handle:
        log_file_handle.write("\n".join(log_buffer) + "\n")
    log_buffer.clear()

def append_to_log_buffer(message):
    log_buffer.append(message)
    if len(log_buffer) >= 10:  # Adjust the buffer size as needed
        flush_log_buffer()

def get_active_window_title():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        window_title = win32gui.GetWindowText(hwnd)
        return process.name(), window_title
    except psutil.NoSuchProcess:
        # Skip the logging if the process no longer exists
        return None, None
    except Exception:
        # Catch any other unexpected errors
        return None, None

def clean_old_logs():
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        new_lines = []
        cutoff_date = datetime.now() - timedelta(days=1)
        
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith("Date:"):
                date_str = line.strip().split()[1]
                try:
                    log_date = datetime.strptime(date_str, '%d/%m/%y')
                    if log_date >= cutoff_date:
                        new_lines.append(line)
                        while i + 1 < len(lines) and not lines[i + 1].strip().startswith("Date:"):
                            new_lines.append(lines[i + 1])
                            i += 1
                except ValueError:
                    new_lines.append(line)
            i += 1
        
        with open(log_file, 'w', encoding='utf-8') as file:
            file.writelines(new_lines)

def log_active_window():
    last_window = None
    last_app_name = None
    start_time = None
    current_date = datetime.now().strftime('%d/%m/%y')

    # Create a new log file if it doesn't exist or write date header if log file is empty
    if not os.path.exists(log_file) or os.path.getsize(log_file) == 0:
        safe_write_log(f"Date: {current_date}")

    clean_old_logs()

    while True:
        app_name, window_title = get_active_window_title()
        current_time = time.time()

        if app_name and window_title and window_title.strip():
            date_str = datetime.fromtimestamp(current_time).strftime('%d/%m/%y')

            # Check the date every 6 hours
            if int(time.time()) % 21600 == 0:  # 21600 seconds = 6 hours
                clean_old_logs()

            # Write the date header if it's a new day
            if date_str != current_date:
                append_to_log_buffer(f"\nDate: {date_str}")
                current_date = date_str

            if window_title != last_window or app_name != last_app_name:
                if last_window and last_app_name:
                    end_time = current_time
                    duration = (end_time - start_time)  # Duration in seconds

                    start_time_formatted = datetime.fromtimestamp(start_time).strftime('%H:%M:%S')
                    end_time_formatted = datetime.fromtimestamp(end_time).strftime('%H:%M:%S')

                    append_to_log_buffer(
                        f"App: {last_app_name} ({last_window}) | "
                        f"Start: {start_time_formatted} | "
                        f"End: {end_time_formatted} | "
                        f"Duration: {duration:.2f} sec"
                    )

                    if last_app_name != app_name:
                        append_to_log_buffer("Task switched")

                start_time = current_time
                last_window = window_title
                last_app_name = app_name

        time.sleep(1)

if __name__ == "__main__":
    log_active_window()