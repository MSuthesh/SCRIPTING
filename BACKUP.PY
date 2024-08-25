import shutil
import os
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import time
import logging

def setup_logging():
    # Generate a timestamp for the log file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file_path = f'C:\\Users\\94776\\Desktop\\python\\backup_script_{timestamp}.log'
    
    # Set up logging configuration
    logging.basicConfig(filename=log_file_path, level=logging.INFO,
                        format='%(asctime)s - %(levelname)s - %(message)s')
    return log_file_path

def backup_files(source_dir, backup_dir):
    start_time = time.time()  # Start timing

    # Check if the source directory exists
    if not os.path.isdir(source_dir):
        logging.error(f"Error: The source directory '{source_dir}' does not exist.")
        return False, None

    # Create backup directory if it doesn't exist
    try:
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
    except Exception as e:
        logging.error(f"Error creating backup directory '{backup_dir}': {e}")
        return False, None

    # Initialize success flag
    success = True
    files_count = 0

    # Iterate over all files in the source directory
    for file_name in os.listdir(source_dir):
        source_file = os.path.join(source_dir, file_name)
        if os.path.isfile(source_file):
            # Prepare backup file name with timestamp
            name, ext = os.path.splitext(file_name)
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            backup_name = f"{name}_{timestamp}{ext}"
            backup_path = os.path.join(backup_dir, backup_name)

            try:
                # Copy the file to the backup directory
                shutil.copy2(source_file, backup_path)
                files_count += 1
                logging.info(f"Successfully backed up file: {file_name}")
            except Exception as e:
                logging.error(f"An error occurred while backing up the file '{file_name}': {e}")
                success = False

    # Calculate duration
    duration = time.time() - start_time

    if success:
        logging.info(f"Backup created successfully for {files_count} files.")
    else:
        logging.warning(f"Backup completed with some errors. Total files backed up: {files_count}")

    return success, duration

def send_email(subject, body, to_email, log_file_path):
    from_email = 'your_email@example.com'  # Replace with your email address
    password = 'your_email_password'        # Replace with your email password
    smtp_server = 'smtp.example.com'        # Replace with your SMTP server
    smtp_port = 587                        # Typically 587 for TLS, 465 for SSL

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach the log file
    try:
        with open(log_file_path, 'rb') as log_file:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(log_file.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition',
                            f'attachment; filename={os.path.basename(log_file_path)}')
            msg.attach(part)
    except Exception as e:
        logging.error(f"An error occurred while attaching the log file: {e}")

    try:
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(from_email, password)
            server.send_message(msg)
        logging.info(f"Email sent successfully to {to_email}")
    except Exception as e:
        logging.error(f"An error occurred while sending the email: {e}")

def main():
    # Set up logging and get the log file path
    log_file_path = setup_logging()
    logging.info(f"Logging started. Log file: {log_file_path}")

    # Define source directory and backup directory
    source_directory = r'C:\Users\94776\Desktop\python\abc'  # Path to your source directory
    backup_directory = r'C:\Users\94776\Desktop\python\dcf'  # Path to your backup directory

    # Perform backup and send email if successful
    success, duration = backup_files(source_directory, backup_directory)
    if success:
        subject = 'Backup Successful'
        body = (f"The backup of the files from '{source_directory}' was created successfully.\n"
                f"Total files backed up: {len(os.listdir(source_directory))}\n"
                f"Time taken for the backup: {duration:.2f} seconds.")
        to_email = 'recipient@example.com'  # Replace with the recipient's email address
        send_email(subject, body, to_email, log_file_path)

if __name__ == "__main__":
    main()
