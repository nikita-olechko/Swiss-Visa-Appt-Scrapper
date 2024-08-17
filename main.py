from datetime import datetime

from SwissScrapper import SwissScrapper


def main():
    # Run every 30 seconds
    run_every_x_seconds = 30

    # Book appointment if available
    book_appointment = True

    # Send SMS on availability.
    send_sms_on_availability = True

    # Send SMS on availability.
    call_user_on_appointment_availability = False

    start_date = datetime(2024, 9, 1)
    end_date = datetime(2024, 9, 15)

    swiss_scrapper = SwissScrapper(run_every_x_seconds=run_every_x_seconds,
                                   book_appointment=book_appointment,
                                   send_sms_on_availability=send_sms_on_availability,
                                   call_user_on_appointment_availability=call_user_on_appointment_availability)

    swiss_scrapper.run_checking_loop(start_date, end_date)


if __name__ == "__main__":
    main()
