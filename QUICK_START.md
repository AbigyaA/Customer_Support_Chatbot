# Quick Start Guide

This guide will help you get the Bank Customer Service Chatbot up and running quickly.

## Prerequisites

⚠️ **IMPORTANT**: Rasa requires **Python 3.8-3.10**. Python 3.11+ is **not supported**.

If you have Python 3.11, 3.12, or 3.13, you need to:
1. Install Python 3.10 from https://www.python.org/downloads/release/python-31011/
2. Or use `pyenv` or `conda` to create a Python 3.10 environment
3. See `SETUP_PYTHON.md` for detailed instructions

- Python 3.10 (recommended) or 3.8-3.9
- pip (Python package manager)

## Installation Steps

### 1. Create Virtual Environment with Python 3.10 (Required)

```bash
# Windows (using Python 3.10)
py -3.10 -m venv venv
venv\Scripts\activate

# macOS/Linux (using Python 3.10)
python3.10 -m venv venv
source venv/bin/activate

# Verify Python version (should show 3.10.x)
python --version
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Train the Model

```bash
rasa train
```

This will create a trained model in the `models/` directory. Training may take a few minutes.

### 4. Start the Action Server

Open a terminal and run:

```bash
rasa run actions
```

Keep this terminal open. The action server will run on `http://localhost:5055/webhook`.

### 5. Start the Rasa Server

Open another terminal and run:

```bash
rasa shell
```

This will start an interactive shell where you can chat with the bot.

## Quick Test

Try these sample queries:

1. **Greeting**: `Hello`
2. **Branch Locator**: `Where is the nearest branch?`
3. **Lost Card**: `I lost my credit card`
4. **Balance Check**: `What's my balance?` (then provide account number: `123456789`)
5. **Human Handoff**: `I want to talk to a human`
6. **Goodbye**: `Bye`

## Alternative: REST API Mode

If you want to use the REST API instead of the shell:

```bash
rasa run --enable-api --cors "*"
```

Then use the test script:

```bash
python test_chatbot.py
```

Or send POST requests to `http://localhost:5005/webhooks/rest/webhook`:

```bash
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "test_user", "message": "Hello"}'
```

## Troubleshooting

### Issue: "Command 'rasa' not found"

**Solution**: Make sure you've activated your virtual environment and installed dependencies:
```bash
pip install -r requirements.txt
```

### Issue: "Action server not found"

**Solution**: Make sure the action server is running on port 5055:
```bash
rasa run actions
```

### Issue: Model not found

**Solution**: Train the model first:
```bash
rasa train
```

### Issue: Port already in use

**Solution**: Change the port:
```bash
rasa shell --port 5006
rasa run actions --port 5056
```

## Next Steps

- Read the [README.md](README.md) for detailed documentation
- Check [ARCHITECTURE.md](ARCHITECTURE.md) for system architecture details
- Customize intents and responses in `data/nlu.yml` and `domain.yml`
- Add more custom actions in `actions/actions.py`

## Project Structure

```
Customer_Support_Chatbot/
├── actions/              # Custom action implementations
│   ├── __init__.py
│   └── actions.py
├── data/                 # Training data
│   ├── nlu.yml          # Intent examples
│   ├── stories.yml      # Conversation flows
│   └── rules.yml        # Conversation rules
├── config.yml           # Rasa configuration
├── domain.yml           # Domain definition
├── credentials.yml      # API credentials
├── endpoints.yml        # Endpoint configuration
├── requirements.txt     # Python dependencies
├── README.md           # Full documentation
├── ARCHITECTURE.md     # Architecture documentation
└── test_chatbot.py     # Test script
```

## Demo Scenarios

### Scenario 1: Check Balance

```
User: What's my balance?
Bot: For security purposes, I need to verify your identity before accessing 
     account information. Please provide your account number or customer ID.

User: 123456789
Bot: Identity verified. Your checking account balance is $5,432.10. 
     Is there anything else I can help with?
```

### Scenario 2: Lost Card

```
User: I lost my credit card
Bot: I'm sorry to hear that your credit card has been lost or stolen. 
     This must be stressful. I can help guide you through the steps to 
     protect your account.

Bot: Here are the steps to secure your account:
     1. Freeze your card immediately to prevent unauthorized use
     2. Report the incident through our online portal or mobile app
     3. Request a replacement card
     4. Monitor your account for any suspicious activity

     For security reasons, I cannot freeze your card directly through this 
     chat. Would you like me to connect you with a human agent who can 
     process these actions immediately?

User: Yes
Bot: I'll connect you with a human agent right away. One moment please...
```

### Scenario 3: Branch Locator

```
User: Find a branch in New York
Bot: The nearest branch is:

     Main Street Branch
     Address: 123 Main Street, New York, NY 10001
     Phone: (212) 555-0100
     Hours: Mon-Fri: 9:00 AM - 5:00 PM, Sat: 9:00 AM - 2:00 PM
```

## Security Notes

⚠️ **Important**: This is a demonstration chatbot with mocked data. In production:

- Implement proper identity verification (MFA, biometrics)
- Use secure API connections (HTTPS/TLS)
- Encrypt sensitive data
- Implement rate limiting
- Add fraud detection
- Enable audit logging

All account data is mocked for demonstration purposes.

## Support

For issues or questions:
- Check Rasa documentation: https://rasa.com/docs/
- Review the architecture documentation in `ARCHITECTURE.md`
- Check Rasa community forums: https://forum.rasa.com/

