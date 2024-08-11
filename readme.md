This project will scrape Swiss consulate visa appointment, provided a url, and will send an SMS/Call you when one is available.

Can be easily modified to book the appointment for you.

The Swiss Consulate does not appear to use Cloudflare, or any web security! Don't worry about rate limiting, at least as of 8/10/2024.

## Installation

1. Clone the repository. Navigate into a new (empty) folder, open Command Prompt (CMD) and run

```bash
git clone [link at the top of this page | root link of the repository]
```

 If you do not have git installed, install it [here](https://www.computerhope.com/issues/ch001927.htm).

2. Navigate into the folder created by the git clone command.  
3. Create a new file called .env. If you are using the version I gave you, just copy paste the provided file. Otherwise using the .env.example file, modify the .env file with your information. You must have an active Twilio account.
4. Install the requirements

On Windows
```bash
python -m ensurepip --upgrade
pip install -r requirements.txt
```

If the 'python' command doesn't work, try 'py' or 'python3' instead.

5. Run the script

On Windows
```bash
python main.py
```
