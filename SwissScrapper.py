import os
import time
from datetime import datetime

from bs4 import BeautifulSoup
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from twilio.rest import Client


class SwissScrapper:
    def __init__(self, run_every_x_seconds=30, call_user_on_appointment_availability=False,
                 send_sms_on_availability=True, book_appointment=True):

        load_dotenv()
        self.url = os.getenv('APPT_URL')
        self.account_sid = os.getenv('TWILIO_ACCOUNT_SID')
        self.auth_token = os.getenv('TWILIO_AUTH_TOKEN')
        self.to_phone_number = os.getenv('TO_PHONE_NUMBER')
        self.from_phone_number = os.getenv('TWILIO_PHONE_NUMBER')
        self.twilio_client = Client(self.account_sid, self.auth_token)
        self.driver = webdriver.Chrome()
        self.run_every_x_seconds = run_every_x_seconds
        self.call_user_on_appointment_availability = call_user_on_appointment_availability
        self.book_appointment = book_appointment
        self.send_sms_on_availability = send_sms_on_availability
        self.date_index = 0

    def check_for_appointments(self, start_date, end_date):

        available_dates = self.get_available_dates()

        first_available_date = None

        self.date_index = 0

        for date in available_dates:

            self.date_index += 1

            date = date.split(" ")[1]
            date_obj = datetime.strptime(date, "%d.%m.%Y")

            if end_date > date_obj > start_date:
                first_available_date = date_obj
                break

        if first_available_date is not None:

            if self.book_appointment:
                self.book_swiss_visa_appointment(first_available_date)

            elif self.send_sms_on_availability:
                self.send_sms(f"First available date is {first_available_date}")
                if self.call_user_on_appointment_availability:
                    self.call_user()

    def book_swiss_visa_appointment(self, date):
        self.send_sms(f"Appointment found on {date}! Attempting to Book...")

        tbody = self.driver.find_element(By.XPATH, "//tbody[@role='rowgroup']")
        first_element = tbody.find_element(By.XPATH, f"./child::*[{self.date_index}]")
        first_element.click()

        # Find button by id, bookBtn
        book_button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'bookBtn')))
        book_button.click()

        self.send_sms(f"Appointment booked on {date}!")

    def get_available_dates(self):

        self.driver.get(self.url)

        # Disable the cache to ensure we get the most up-to-date information
        self.driver.execute_cdp_cmd("Network.setCacheDisabled", {"cacheDisabled": True})

        # Not always necessary. TODO: actually check for these elements instead and operate dynamically.
        # button = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'rebookBtn')))
        # button.click()

        button = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.ID, 'bookingListBtn')))
        button.click()

        # Wait for the <app-root> element to load
        root_element = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'app-root')))

        # Wait for the content inside <app-root> to load (this may vary based on the specific webpage)
        time.sleep(2)
        content = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, 'app-proposal-table')))

        # Get the entire HTML inside <app-root>
        html_data = root_element.get_attribute('outerHTML')

        # Print the HTML content of the table
        # print(html_data)

        soup = BeautifulSoup(html_data, 'html.parser')

        # Find elements containing the dates
        date_elements = soup.find_all(class_="cdk-column-proposalDate")

        # Extract and print the dates
        available_dates = [date.text.strip() for date in date_elements]

        available_dates = available_dates[1:]

        return available_dates

    def send_sms(self, message):
        try:
            self.twilio_client.messages.create(
                to=self.to_phone_number,
                from_=self.from_phone_number,
                body=message
            )
            print("Text Sent!")
        except Exception as e:
            print("Text not sent. Error:", str(e))

    def call_user(self):
        try:
            self.twilio_client.calls.create(
                to=self.to_phone_number,
                from_=self.from_phone_number,
                url='http://demo.twilio.com/docs/voice.xml'
            )
            print("Calling!")
        except Exception as e:
            print("Call not made. Error:", str(e))

    def run_checking_loop(self, start_date, end_date):
        times_checked = 0
        while True:
            try:
                times_checked += 1
                self.check_for_appointments(start_date, end_date)
                print(f"Checked {times_checked} times. Last checked at {datetime.now()}")
            except Exception as e:
                print(str(e))
                break
            time.sleep(self.run_every_x_seconds)

