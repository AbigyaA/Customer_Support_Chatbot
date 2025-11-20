# Bank Customer Service Chatbot

A conversational AI chatbot built with Rasa for bank customer service, handling account inquiries, branch location, lost card assistance, and general FAQs.

## Features

- **Account Balance Check** (with identity verification, mocked data)
- **Recent Transactions View** (with identity verification, mocked data)
- **Branch Locator** (finds nearest branch based on location)
- **Lost/Stolen Card Assistance** (guided flow without direct actions)
- **General Banking FAQs** (answers common banking questions)
- **Human Agent Handoff** (seamless escalation when requested)
- **Identity Verification** (security measures for sensitive information)

## Project Structure

```
Customer_Support_Chatbot/
├── actions/
│   ├── __init__.py
│   └── actions.py          # Custom action implementations
├── data/
│   ├── nlu.yml            # Intent training data with sample utterances
│   ├── stories.yml        # Conversation flows
│   └── rules.yml          # Conversation rules
├── config.yml             # Rasa configuration (NLU pipeline, policies)
├── domain.yml             # Domain definition (intents, entities, responses, actions)
├── credentials.yml        # API credentials configuration
├── endpoints.yml          # Action server and tracker store endpoints
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

## Installation

⚠️ **Important**: Rasa requires Python 3.8-3.10. Python 3.11, 3.12, and 3.13 are **not yet supported**.

If you have Python 3.11+, please:
1. Install Python 3.10 from https://www.python.org/downloads/release/python-31011/
2. Or see `SETUP_PYTHON.md` for detailed setup instructions

1. **Install Python 3.10** (required for Rasa compatibility)

2. **Create a virtual environment** with Python 3.10 (recommended):
```bash
# Using Python 3.10 specifically
py -3.10 -m venv venv  # On Windows
# OR
python3.10 -m venv venv  # On macOS/Linux

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Install Rasa** (if not already installed via requirements.txt):
```bash
pip install rasa==3.6.15
```

## Running the Chatbot

### 1. Train the Model

```bash
rasa train
```

This will create a trained model in the `models/` directory.

### 2. Start the Action Server

In one terminal window, start the Rasa action server:

```bash
rasa run actions
```

The action server will run on `http://localhost:5055/webhook` by default.

### 3. Start the Rasa Server

In another terminal window, start the Rasa server:

```bash
rasa shell
```

This will start an interactive shell where you can chat with the bot.

### Alternative: Run with REST API

```bash
rasa run --enable-api --cors "*"
```

Then interact via API calls or use Rasa X/web interface.

## Architecture Documentation

### 1. Intents

The chatbot recognizes the following intents:

| Intent | Description | Example Utterances |
|--------|-------------|-------------------|
| `greet` | User greeting | "hello", "hi", "good morning" |
| `goodbye` | User farewell | "bye", "see you later" |
| `affirm` | Positive confirmation | "yes", "sure", "okay" |
| `deny` | Negative response | "no", "nope" |
| `check_balance` | Request account balance | "what's my balance", "check my account balance" |
| `view_transactions` | Request transaction history | "show my recent transactions", "transaction history" |
| `branch_locator` | Find nearby branch | "find a branch", "where is the nearest branch" |
| `lost_card` | Report lost/stolen card | "i lost my card", "card got stolen", "my card was stolen" |
| `freeze_card` | Request to freeze card | "freeze my card", "block my card" |
| `general_faq` | General banking questions | "what are your hours", "how do i transfer money" |
| `request_human` | Request human agent | "i want to talk to a human", "this isn't helping" |
| `verify_identity` | Provide verification info | "my account number is 123456" |
| `unknown_query` | Unrecognized input | Fallback intent |

### 2. Entities

Entities extracted from user messages:

- `account_type`: Type of account (checking, savings)
- `card_type`: Type of card (credit card, debit card)
- `branch_location`: Location for branch search (e.g., "New York", "downtown")
- `account_number`: Account number for verification (extracted via pattern matching)

### 3. Slots

Slots used to maintain conversation state:

- `account_type`: Current account type in context
- `card_type`: Current card type in context
- `identity_verified`: Boolean flag for verified identity
- `requested_action`: Action pending identity verification
- `verification_attempts`: Count of failed verification attempts
- `branch_location`: Location for branch search

### 4. Custom Actions

#### `action_check_balance`
- **Purpose**: Retrieves and displays account balance
- **Security**: Requires `identity_verified = True`
- **Backend**: Uses mocked data (in production, would query database/API)
- **Response**: Returns balance formatted as currency

#### `action_view_transactions`
- **Purpose**: Retrieves and displays recent transactions
- **Security**: Requires `identity_verified = True`
- **Backend**: Uses mocked transaction data
- **Response**: Returns formatted list of recent transactions

#### `action_branch_locator`
- **Purpose**: Finds nearest branch based on location
- **Security**: No verification required (public information)
- **Backend**: Uses mocked branch database
- **Response**: Returns branch details (name, address, phone, hours)

#### `action_verify_identity`
- **Purpose**: Verifies user identity before sensitive operations
- **Method**: Accepts account number (6+ digits) - mocked verification
- **Limits**: Maximum 3 attempts before escalation
- **Response**: Sets `identity_verified` slot to True/False

#### `action_lost_card_flow`
- **Purpose**: Handles lost/stolen card scenario
- **Security**: Provides guidance only, no direct actions
- **Response**: Empathy message + step-by-step instructions + handoff offer

#### `action_general_faq`
- **Purpose**: Answers common banking questions
- **Method**: Keyword-based matching (can be enhanced with knowledge base)
- **Response**: Returns relevant FAQ answer

#### `action_fallback_handler`
- **Purpose**: Handles unknown queries
- **Method**: Provides helpful fallback message
- **Enhancement**: Can integrate GPT-based component (see below)

### 5. Conversation Flows (Stories)

The chatbot implements several conversation flows:

1. **Balance Check Flow**: Greet → Request Balance → Verify Identity → Show Balance
2. **Transaction View Flow**: Request Transactions → Verify Identity → Show Transactions
3. **Branch Locator Flow**: Request Branch → Show Branch Details
4. **Lost Card Flow**: Report Lost Card → Empathy → Steps → Offer Handoff
5. **FAQ Flow**: Ask Question → Provide Answer
6. **Human Handoff Flow**: Request Agent → Connect to Human

### 6. Security Measures

#### Identity Verification
- **Requirement**: All account-specific information requires verification
- **Method**: Account number validation (mocked - accepts 6+ digit numbers)
- **Limits**: Maximum 3 verification attempts
- **Escalation**: Failed verification offers human agent handoff

#### Sensitive Actions
- **Policy**: Bot does NOT perform sensitive actions directly
- **Examples**: Cannot freeze cards, cannot transfer money, cannot change account details
- **Behavior**: Provides instructions and offers human agent connection

#### Data Handling
- **Mocked Data**: All account data is mocked for demonstration
- **Production**: Would require secure API connections with encryption
- **Storage**: No sensitive data stored in conversation logs

### 7. Human Agent Handoff

The chatbot recognizes when to hand off to a human agent:

**Explicit Requests:**
- User says "I want to talk to a human"
- User says "This isn't helping"
- User requests "agent" or "representative"

**Automatic Escalation:**
- Failed identity verification (3+ attempts)
- User frustration detected (could be enhanced with sentiment analysis)

**Handoff Process:**
1. Acknowledge request
2. Apologize for inability to help
3. Offer immediate connection
4. Transfer to agent queue (mocked in demo)

## Sample Conversations

### Example 1: Check Balance
```
User: Hello
Bot: Hello! I'm your bank's virtual assistant. How can I help you today?

User: What's my balance?
Bot: For security purposes, I need to verify your identity before accessing account 
     information. Please provide your account number or customer ID.

User: My account number is 123456789
Bot: Identity verified successfully. How can I assist you?
     Your checking account balance is $5,432.10.

User: Thanks, bye
Bot: Thank you for contacting us. Have a great day!
```

### Example 2: Lost Card
```
User: I lost my credit card
Bot: I'm sorry to hear that your credit card has been lost or stolen. This must be 
     stressful. I can help guide you through the steps to protect your account.

Bot: Here are the steps to secure your account:
     1. Freeze your card immediately to prevent unauthorized use
     2. Report the incident through our online portal or mobile app
     3. Request a replacement card
     4. Monitor your account for any suspicious activity

     For security reasons, I cannot freeze your card directly through this chat. 
     Would you like me to connect you with a human agent who can process these 
     actions immediately?

User: Yes
Bot: I'll connect you with a human agent right away. One moment please...
```

### Example 3: Branch Locator
```
User: Where is the nearest branch?
Bot: The nearest branch is:

     Central Branch
     Address: 789 Bank Avenue, New York, NY 10003
     Phone: (212) 555-0300
     Hours: Mon-Fri: 9:00 AM - 5:00 PM, Sat: 9:00 AM - 2:00 PM

User: Thanks!
Bot: Is there anything else I can help with?
```

### Example 4: Human Handoff
```
User: This isn't helping, I need to talk to someone
Bot: I'll connect you with a human agent right away. One moment please...
```

## NLP: Recognizing Variations

The chatbot uses Rasa's DIET classifier to recognize variations of user input:

- **Lost Card Variations**: "lost my card", "card got stolen", "card was stolen", 
  "someone stole my card", "my card is missing" all trigger the `lost_card` intent
- **Balance Variations**: "what's my balance", "check balance", "how much do I have", 
  "account balance" all trigger `check_balance` intent
- **Handoff Variations**: "i want to talk to a human", "this isn't helping", 
  "connect me to an agent" all trigger `request_human` intent

This is achieved through:
1. **Training Data**: Multiple example utterances per intent in `data/nlu.yml`
2. **DIET Classifier**: Neural network that learns semantic similarities
3. **Entity Extraction**: Recognizes entities in context (e.g., "credit card" vs "debit card")

## Backend Integration (Mocked)

The current implementation uses mocked data. In production, actions would connect to:

### Database/API Endpoints

1. **Account Service API**
   - `GET /api/accounts/{accountId}/balance` - Get account balance
   - `GET /api/accounts/{accountId}/transactions` - Get recent transactions
   - `POST /api/identity/verify` - Verify customer identity

2. **Branch Service API**
   - `GET /api/branches?location={location}` - Find nearby branches
   - `GET /api/branches/{branchId}` - Get branch details

3. **Card Service API**
   - `POST /api/cards/{cardId}/freeze` - Freeze card (not directly called by bot)
   - `GET /api/cards/{cardId}/status` - Get card status

4. **Knowledge Base**
   - `GET /api/faq/search?query={query}` - Search FAQ database

### Integration Example (Pseudocode)

```python
# In actions/actions.py - action_check_balance

import requests

def run(self, dispatcher, tracker, domain):
    identity_verified = tracker.get_slot("identity_verified")
    
    if not identity_verified:
        # Request verification
        return
    
    account_id = tracker.get_slot("account_id")
    
    # Real API call
    response = requests.get(
        f"https://api.bank.com/accounts/{account_id}/balance",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    balance = response.json()["balance"]
    dispatcher.utter_message(text=f"Your balance is ${balance}")
```

## GPT-Based Component (Optional)

A GPT-based fallback handler can be integrated for unknown queries. **See `actions/actions.py` for commented example.**

### Implementation Considerations

**Guardrails Required:**
1. **System Prompt Restrictions**: 
   - Never provide account numbers or sensitive data
   - Never perform transactions
   - Always require verification for account info
   - Offer human handoff when unsure

2. **Output Filtering**:
   - Check for sensitive keywords in responses
   - Block responses containing account numbers, SSNs, PINs
   - Limit response length to prevent hallucinations

3. **Context Awareness**:
   - Include conversation history carefully
   - Don't include sensitive slots/entities in prompts
   - Reset context for each sensitive operation

4. **Error Handling**:
   - Fallback to rule-based handler on API failures
   - Rate limiting to prevent abuse
   - Cost monitoring

### Risks Without Guardrails

1. **Data Leakage**: GPT might generate or expose sensitive information
2. **Unauthorized Actions**: User might trick GPT into "performing" actions
3. **Hallucinations**: GPT might provide incorrect financial advice
4. **Context Bleeding**: Sensitive information might leak into future conversations
5. **Cost**: Unbounded API calls could be expensive
6. **Compliance**: May violate banking regulations without proper controls

### Recommended Approach

- Use GPT **only** for general FAQ fallback
- **Never** use GPT for account-specific queries
- Implement strict filtering and monitoring
- Regular audits of GPT responses
- Clear user notice that AI-generated responses may be inaccurate

## Testing

### Test Conversation Flows

```bash
# Interactive testing
rasa shell

# Test specific stories
rasa test

# Test NLU only
rasa test nlu
```

### Manual Testing Checklist

- [ ] Balance check with verification
- [ ] Balance check without verification (should prompt)
- [ ] Transaction view with verification
- [ ] Branch locator with location
- [ ] Branch locator without location (default)
- [ ] Lost card report
- [ ] Lost card variation: "stolen"
- [ ] Freeze card request (should not perform action)
- [ ] General FAQ queries
- [ ] Human handoff request
- [ ] Failed verification (3 attempts)
- [ ] Unknown query fallback

## Deployment

### Production Deployment Options

1. **Rasa X**: Web interface for managing conversations and training
2. **Rasa Server**: REST API for integration with custom frontend
3. **Docker**: Containerized deployment
4. **Cloud Platforms**: AWS, Azure, GCP with serverless options

### Environment Variables

```bash
# Action server
ACTION_SERVER_URL=http://localhost:5055

# Database (if using)
DATABASE_URL=postgresql://user:pass@localhost/rasa

# External APIs
BANK_API_URL=https://api.bank.com
BANK_API_KEY=your_api_key

# GPT (if enabled)
OPENAI_API_KEY=your_openai_key
```

## Future Enhancements

1. **Multi-language Support**: Add support for multiple languages
2. **Voice Interface**: Integrate with voice assistants
3. **Sentiment Analysis**: Detect user frustration for automatic handoff
4. **Proactive Messaging**: Notify users about suspicious activity
5. **Knowledge Base Integration**: Connect to comprehensive FAQ database
6. **Analytics**: Track common queries and improve responses
7. **A/B Testing**: Test different conversation flows
8. **Voice Biometrics**: Enhanced identity verification

## License

This project is for educational/demonstration purposes.

## Contact

For questions or issues, please refer to Rasa documentation: https://rasa.com/docs/

