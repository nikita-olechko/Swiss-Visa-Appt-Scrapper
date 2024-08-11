This project will scrape Swiss consulate visa appointment, provided a url, and will send an SMS/Call you when one is available.

Can be easily modified to book the appointment for you.

The Swiss Consulate does not appear to use cloudflare! This is lovely for bots. Don't really worry about rate limiting, at least as of 8/10/2024.

## Installation

1. Clone the repository
2. Modify the .env file with your information. You must have an active Twilio account.
3. Install the requirements

On Windows
```bash
python -m ensurepip --upgrade
pip install -r requirements.txt
```

4. Run the script

On Windows
```bash
python main.py
```
