import os
import glob
import time

# Configuration
log_directory = r'C:\Users\94776\Desktop\python'  # Directory where log files are stored
log_file_pattern = 'backup_script_*.log'  # Pattern for log files
max_file_age_days = 3  # Maximum age of log files to retain (in days)

def cleanup_logs(log_dir, file_pattern, max_age_days):
    # Get the current time
    now = time.time()

    # Find all log files that match the pattern
    log_files = glob.glob(os.path.join(log_dir, file_pattern))

    # Filter out files based on age
    old_files = []
    for log_file in log_files:
        file_age_days = (now - os.path.getmtime(log_file)) / (60 * 60 * 24)
        if file_age_days > max_age_days:
            old_files.append(log_file)

    # Delete old files
    for old_file in old_files:
        try:
            os.remove(old_file)
            print(f"Deleted old log file: {old_file}")
        except Exception as e:
            print(f"Failed to delete {old_file}: {e}")

def main():
    cleanup_logs(log_directory, log_file_pattern, max_file_age_days)

if __name__ == "__main__":
    main()
