import os
import time
from datetime import datetime

from dotenv import load_dotenv
from selenium import webdriver
from bs4 import BeautifulSoup
from twilio.rest import Client

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# CONFIGURE HERE!!

# Target date in the format (year, month, day). Will send when there is an appointment before this date.
target_date = datetime(2024, 9, 15)

# Set to True if you want to call the user as well as text them.
call_user = False

# How often to check for appointments in seconds.
run_every_x_seconds = 30


def check_dates(target_date, call_user):
    load_dotenv()
    available_dates = []
    notifications = 0
    # Initialize a WebDriver (for Chrome)
    driver = webdriver.Chrome()  # You will need to download and specify the path to the Chrome driver executable.

    URL = os.getenv('APPT_URL')
    driver.get(URL)

    # Your Twilio Account SID and Auth Token
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')

    # Create a Twilio client
    client = Client(account_sid, auth_token)

    # The phone number to send the message to (must be in E.164 format)
    to_phone_number = os.getenv('TO_PHONE_NUMBER')

    # Your Twilio phone number
    from_phone_number = os.getenv('TWILIO_PHONE_NUMBER')

    try:
        # Not always necessary. TODO: actually check for these elements instead and operate dynamically.
        # button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'rebookBtn')))
        # button.click()

        button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'bookingListBtn')))
        button.click()

        # Wait for the <app-root> element to load
        root_element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'app-root')))

        # Wait for the content inside <app-root> to load (this may vary based on the specific webpage)
        time.sleep(2)
        content = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'app-proposal-table')))

        # Get the entire HTML inside <app-root>
        html_data = root_element.get_attribute('outerHTML')

        # Print the HTML content of the table
        # print(html_data)

        soup = BeautifulSoup(html_data, 'html.parser')

        # Find elements containing the dates
        date_elements = soup.find_all(class_="cdk-column-proposalDate")

        # Extract and print the dates
        available_dates = [date.text.strip() for date in date_elements]

    except Exception as e:
        print(f"Error: {e}")

    print("Available dates:")
    available_dates = available_dates[1:]
    message = "Date too late"
    for date in available_dates:
        date = date.split(" ")[1]
        print(date)
        date_obj = datetime.strptime(date, "%d.%m.%Y")

        if date_obj < target_date:

            try:
                # Message to send
                client.messages.create(
                    to=to_phone_number,
                    from_=from_phone_number,
                    body='There is a Swiss-Visa appointment available on ' + date
                         + ' at the Swiss Consulate! Go sign up!'
                )
                print("Text Sent!")
                notifications += 1
            except Exception as e:
                print("Text not sent. Error:", str(e))
            if call_user:
                try:
                    client.calls.create(
                        to=to_phone_number,  # Recipient's phone number
                        from_=from_phone_number,
                        url='http://demo.twilio.com/docs/voice.xml'
                    )
                    print("Calling!")
                    notifications += 1
                except Exception as e:
                    print("Call not made. Error:", str(e))
            return notifications
    if message == "Date too late":
        print(f"Dates are too late. Text not sent.\n")
    # Close the browser when you're done
    print("Closing Program")
    time.sleep(5)
    driver.quit()
    return notifications


if __name__ == "__main__":
    texts_sent = 0
    while True:
        try:
            texts_sent += check_dates(target_date, call_user)
        except Exception as e:
            print("An error occurred: ", str(e))
        time.sleep(run_every_x_seconds)
        if texts_sent >= 1:
            print(
                f"2 Notifications Sent. That's enough for now. Start again in 30 seconds\n. Current time is {datetime.now()}")
            time.sleep(30)
            texts_sent = 0
