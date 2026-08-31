# WhatsApp Web Monitor - Python Prototype

A small learning prototype that uses Selenium to observe WhatsApp Web and save selected incoming message data locally as JSON.

## What It Does

- Opens WhatsApp Web in Chrome
- Reuses a local browser profile after QR authentication
- Watches the currently available chat interface for incoming messages
- Extracts basic message information exposed by the page
- Stores structured records in a local JSON file

## Tech Stack

- Python
- Selenium
- webdriver-manager
- JSON

## Getting Started

```bash
pip install -r requirements.txt
python bot.py
```

Chrome must be installed. On the first run, scan the WhatsApp Web QR code. Session files and captured messages remain local and are excluded by `.gitignore`.

## My Role

I built the browser-automation flow, session reuse, DOM monitoring, message parsing, and local JSON persistence as an automation exercise.

## Project Status and Limitations

This is a learning/automation prototype, not a production bot. It does not send replies or provide a supported WhatsApp Business integration. WhatsApp Web DOM changes can break selectors, and collected message data must be handled in accordance with user consent and applicable privacy rules.

## License

No open-source license has been declared.
