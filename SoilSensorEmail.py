# Use Comments
# Program Title:Soil moisture detection and email sending
# Program  Description:Monitor the soil condition, send emails to the owner regularly to inform them of the plant situation and determine whether watering is needed
# Name:Yuchen Zhang
# Student ID:20108616
# Course & Year:Project Semester3 
# Date:20/4/2025

import smtplib
from email.message import EmailMessage
import RPi.GPIO as GPIO
import time
from datetime import datetime, timedelta
import pytz

# Soil Sensor Reading Function
def read_soil_moisture():
    # Assuming the sensor is connected to GPIO 4 (BCM numbering)
    DO = 4
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DO, GPIO.IN)

    # Read digital output of the sensor
    moisture_level = GPIO.input(DO)
    return moisture_level

# Email Sending Function
def send_email(plant_status):
    from_email_addr = "3394601452@qq.com"  # Replace with your email address
    from_email_pass = "zcmsurwgnavjdacd"  # Use an app password if necessary
    to_email_addr = "3394601452@qq.com"  # Replace with recipient's email address

    msg = EmailMessage()
    body = f"Plant Status: {plant_status}"
    msg.set_content(body)

    msg['Subject'] = 'Plant Moisture Level'
    msg['From'] = from_email_addr
    msg['To'] = to_email_addr

    try:
        server = smtplib.SMTP_SSL('smtp.qq.com', 465)  # QQ Mail SMTP Server and Port
        server.login(from_email_addr, from_email_pass)
        server.send_message(msg)
        print(f'Email sent: Plant Status - {plant_status}')
    except Exception as e:
        print(f'Failed to send email: {e}')
    finally:
        server.quit()

# Main Script Logic
def main():
    # Define daily reading times in Beijing Time (CST)
    reading_times = ["13:00", "15:00", "18:00", "20:00"]
    
    # Log file to store email history
    log_file = "email_history.txt"

    # Set timezone to Beijing Time
    beijing_tz = pytz.timezone('Asia/Shanghai')

    # Run for 3 days
    for day in range(3):
        print(f"Day {day + 1} Monitoring Started")
        for reading_time in reading_times:
            # Calculate the next reading time in Beijing Time
            now = datetime.now(beijing_tz)  # Current time in Beijing Time
            target_time = datetime.strptime(reading_time, "%H:%M")
            target_time = now.replace(
                hour=target_time.hour,
                minute=target_time.minute,
                second=0,
                microsecond=0
            )
            if target_time < now:
                target_time += timedelta(days=1)  # If the time has passed, schedule for the next day

            wait_time = (target_time - now).total_seconds()
            print(f"Waiting until {target_time.strftime('%Y-%m-%d %H:%M:%S')} (Beijing Time)...")
            time.sleep(wait_time)

            # Take a soil moisture reading
            moisture_level = read_soil_moisture()

            # Determine plant status based on moisture level
            if moisture_level == 0:
                plant_status = "Water NOT needed"
            else:
                plant_status = "Please water your plant"

            # Send email with plant status
            send_email(plant_status)

            # Log the email history
            with open(log_file, "a") as f:
                timestamp = datetime.now(beijing_tz).strftime("%Y-%m-%d %H:%M:%S")
                f.write(f"{timestamp} - {plant_status}\n")

            print(f"Soil Moisture: {'Dry' if moisture_level != 0 else 'Wet'}, Status: {plant_status}")

        print(f"Day {day + 1} Monitoring Completed\n")

if __name__ == "__main__":
    main()
