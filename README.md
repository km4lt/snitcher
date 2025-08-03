# Snitcher

**Snitcher** is a stealthy Windows-based activity logger that monitors and records active application usage with timestamps and durations.

## Goal

The objective behind **Snitcher** is to track which applications are actively used on a Windows system—when, for how long, and in what sequence—without user interaction or visible output. Useful for usage analytics, productivity tracking, or parental monitoring.

## Libraries Used

- **psutil**: For process and system-related information.
- **win32gui** and **win32process**: To access the active window and its associated process.
- **os**, **time**, **datetime**: For file handling and time tracking.

## Features

- Tracks application name and window title  
- Logs start and end times with accurate durations  
- Detects and logs task switches  
- Groups logs by date  
- Buffered writes to reduce I/O  
- Auto-prunes logs older than 1 day every 6 hours

### Example Log Entry

App: chrome.exe (ChatGPT - Google Chrome) | Start: 13:00:05 | End: 13:07:13 | Duration: 428.00 sec
Task switched



## Installation

1. Make sure Python 3.x is installed.
2. Install required packages:

    ```bash
    pip install psutil pywin32
    ```

3. Run the script:

    ```bash
    python snitcher.py
    ```

## Notes

- Works only on Windows due to dependency on `pywin32`.
- Log file is stored at `C:\WindowsX86\app_usage.log`.

## Disclaimer

This script is intended for ethical and legal use only. Do not use it to monitor others without explicit consent.
