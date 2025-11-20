# Bank Customer Service Chatbot - Architecture Documentation

## Table of Contents
1. [Overview](#overview)
2. [System Architecture](#system-architecture)
3. [Intent Recognition](#intent-recognition)
4. [Sample Utterances](#sample-utterances)
5. [Entities](#entities)
6. [Dialogue Management](#dialogue-management)
7. [Custom Actions](#custom-actions)
8. [Backend Integration](#backend-integration)
9. [Security Architecture](#security-architecture)
10. [Human Handoff Mechanism](#human-handoff-mechanism)

---

## 1. Overview

This document describes the architecture of a conversational AI chatbot built with Rasa for bank customer service. The chatbot handles account inquiries, branch location services, lost card assistance, and general banking FAQs while maintaining security through identity verification mechanisms.

### Key Features
- **Account Balance Check** (with identity verification)
- **Recent Transactions View** (with identity verification)
- **Branch Locator** (public information, no verification required)
- **Lost/Stolen Card Assistance** (guided flow without direct actions)
- **General Banking FAQs** (public information)
- **Human Agent Handoff** (seamless escalation)
- **Identity Verification System** (security measures)

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              (Text-based Chat Interface)                 │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP/REST
                     ▼
┌─────────────────────────────────────────────────────────┐
│                   Rasa Core Server                      │
│  ┌────────────────┐         ┌─────────────────────┐   │
│  │   NLU Module   │────────▶│  Dialogue Manager   │   │
│  │   (DIET)       │         │  (TED Policy)       │   │
│  └────────────────┘         └──────────┬──────────┘   │
│                                        │                │
│  ┌─────────────────────────────────────▼──────────┐   │
│  │         Conversation Tracker                   │   │
│  │  (Slots: identity_verified, requested_action)  │   │
│  └────────────────────────────────────────────────┘   │
└───────────────────────────┬────────────────────────────┘
                            │
                            │ HTTP/REST
                            ▼
┌─────────────────────────────────────────────────────────┐
│                  Action Server                          │
│              (Custom Python Actions)                    │
└──────────────┬───────────────────────────┬──────────────┘
               │                           │
               │                           │
       ┌───────▼────────┐         ┌───────▼────────┐
       │  Account       │         │  Branch        │
       │  Service API   │         │  Service API   │
       │  (Mocked)      │         │  (Mocked)      │
       └────────────────┘         └────────────────┘
```

### 2.2 Component Description

#### **Rasa Core Server**
- Handles natural language understanding (NLU)
- Manages conversation flow and dialogue state
- Processes user intents and entities
- Routes to appropriate actions

#### **Action Server**
- Executes custom business logic
- Connects to backend systems (currently mocked)
- Handles identity verification
- Returns formatted responses

#### **Backend Services** (Currently Mocked)
- Account Service: Balance and transaction data
- Branch Service: Branch location information
- Card Service: Card status (not directly accessed by bot)

---

## 3. Intent Recognition

### 3.1 Intent Categories

The chatbot recognizes **14 distinct intents** organized into the following categories:

#### **Account Management Intents**
1. **`check_balance`** - User requests account balance information
2. **`view_transactions`** - User requests transaction history

#### **Service Intents**
3. **`branch_locator`** - User wants to find branch locations
4. **`general_faq`** - User asks general banking questions

#### **Incident Management Intents**
5. **`lost_card`** - User reports lost or stolen card
6. **`freeze_card`** - User wants to freeze/block card

#### **Meta Intents**
7. **`greet`** - User greeting
8. **`goodbye`** - User farewell
9. **`affirm`** - Positive confirmation (yes, sure, okay)
10. **`deny`** - Negative response (no, nope)
11. **`request_human`** - User requests human agent
12. **`verify_identity`** - User provides identity information
13. **`provide_verification`** - User provides verification credentials
14. **`unknown_query`** / **`nlu_fallback`** - Unrecognized or low-confidence queries

### 3.2 NLP Pipeline

The chatbot uses Rasa's default NLU pipeline:

```yaml
Pipeline:
  1. WhitespaceTokenizer - Tokenizes input into words
  2. LexicalSyntacticFeaturizer - Creates lexical/syntactic features
  3. CountVectorsFeaturizer - Creates bag-of-words features
  4. DIETClassifier - Dual Intent and Entity Transformer
     - Epochs: 100
     - Handles intent classification and entity extraction
  5. EntitySynonymMapper - Maps entities to canonical forms
  6. ResponseSelector - Selects appropriate responses
  7. FallbackClassifier - Detects low-confidence predictions
     - Threshold: 0.3 (30% confidence required)
```

---

## 4. Sample Utterances

### 4.1 Account Management

#### **Intent: `check_balance`**

**Sample Utterances:**
- "What's my balance?"
- "Check my account balance"
- "How much money do I have?"
- "Show me my balance"
- "What's my account balance"
- "Balance check"
- "Check balance"
- "I want to see my balance"
- "Can you tell me my balance"
- "What is my current balance"
- "Check my savings account balance"
- "Balance on my checking account"
- "How much is in my savings account"
- "Show balance for my checking account"

**Variations Recognized:**
- Account type variations: "savings", "checking"
- Question format variations: "what's", "show me", "check"
- Formal vs. informal language

#### **Intent: `view_transactions`**

**Sample Utterances:**
- "Show my recent transactions"
- "What are my recent transactions"
- "Transaction history"
- "Recent transactions"
- "Show transactions"
- "View my transactions"
- "Last transactions"
- "Transaction list"
- "I want to see my transactions"
- "Can you show my transaction history"
- "Recent activity"
- "Show me recent activity on my account"

### 4.2 Service Intents

#### **Intent: `branch_locator`**

**Sample Utterances:**
- "Find a branch"
- "Where is the nearest branch"
- "Branch location"
- "Locate branch"
- "Find branch near me"
- "Where's the closest branch"
- "Branch locator"
- "Show me branches"
- "What branches are nearby"
- "I need to visit a branch"
- "Find branch in New York"
- "Nearest branch to downtown"
- "Branch near 123 Main St"

**Entity Extraction:**
- `branch_location`: "New York", "downtown", "123 Main St"

### 4.3 Incident Management

#### **Intent: `lost_card`**

**Sample Utterances:**
- "I lost my card"
- "My card is lost"
- "I lost my credit card"
- "My debit card is missing"
- **"Card got stolen"**
- "Someone stole my card"
- "My card was stolen"
- "I can't find my card"
- "My card disappeared"
- "Card is gone"
- "I think my card is stolen"
- "My credit card got stolen"
- "Someone took my debit card"
- "Lost my credit card"
- "Misplaced my card"
- "Card missing"

**Key Feature:** The chatbot recognizes **semantic variations**:
- "Lost" vs. "stolen" vs. "missing" → All trigger `lost_card` intent
- NLP variations are handled through training data and DIET classifier

**Entity Extraction:**
- `card_type`: "credit card", "debit card"

#### **Intent: `freeze_card`**

**Sample Utterances:**
- "Freeze my card"
- "I want to freeze my card"
- "Can you freeze my card"
- "Block my card"
- "Disable my card"
- "Deactivate my card"
- "Stop my card"
- "Freeze my credit card"
- "Block my debit card"
- "I need to freeze my card immediately"
- "Suspend my card"
- "Cancel my card"

### 4.4 Meta Intents

#### **Intent: `greet`**
- "Hello", "Hi", "Hey", "Good morning", "Good afternoon", "Greetings"

#### **Intent: `goodbye`**
- "Bye", "Goodbye", "See you later", "Farewell", "Have a nice day"

#### **Intent: `affirm`**
- "Yes", "Yep", "Yeah", "Sure", "Absolutely", "Correct", "Okay", "Ok"

#### **Intent: `deny`**
- "No", "Nope", "Not really", "No thanks", "Nah", "No way"

#### **Intent: `request_human`**

**Sample Utterances:**
- "I want to talk to a human"
- "Can I speak with someone"
- "Connect me to an agent"
- "I need a real person"
- "Talk to a person"
- "Human agent"
- "Speak to representative"
- **"This isn't helping"**
- "This bot isn't helping"
- "I need to talk to someone"
- "Can I talk to a human agent"
- "Transfer me to a person"
- "Connect me with support"
- "I want human assistance"
- "Agent please"
- "This isn't working I need help"

#### **Intent: `provide_verification`**

**Sample Utterances:**
- "123456789"
- "My account number is 123456789"
- "789012"
- "My account is 789012"
- "CUST123"
- "345678"
- "Account 901234"
- "987654321"

**Entity Extraction:**
- `account_number`: Numeric values (6+ digits)
- `customer_id`: Alphanumeric IDs (e.g., "CUST123")

### 4.5 General FAQs

#### **Intent: `general_faq`**

**Sample Topics:**
- Banking hours: "What are your hours", "Banking hours", "When are you open"
- Services: "What services do you offer", "Tell me about your services"
- Account opening: "How do I open an account"
- Minimum balance: "What is the minimum balance"
- Interest rates: "Interest rates", "What are your rates"
- Fees: "What are your fees"
- Transfers: "How do I transfer money"
- Bill payment: "How to pay bills"
- Password: "How can I change my password", "Reset password"
- Address update: "How do I update my address"
- Mobile banking: "Mobile banking"
- Online banking: "Online banking", "What can I do with online banking"

---

## 5. Entities

### 5.1 Entity Types

The chatbot extracts the following entities from user input:

| Entity | Type | Description | Examples |
|--------|------|-------------|----------|
| `account_type` | Text | Type of bank account | "savings", "checking" |
| `card_type` | Text | Type of card | "credit card", "debit card" |
| `branch_location` | Text | Location for branch search | "New York", "downtown", "123 Main St" |
| `account_number` | Text | Account number for verification | "123456789", "987654321" |
| `customer_id` | Text | Customer identifier | "CUST123", "CUST67890" |
| `verification_method` | Text | Method of verification | Not currently used |

### 5.2 Entity Extraction Examples

**Example 1: Account Type Extraction**
```
User: "Check my savings account balance"
Intent: check_balance
Entities: 
  - account_type: "savings"
```

**Example 2: Card Type Extraction**
```
User: "I lost my credit card"
Intent: lost_card
Entities:
  - card_type: "credit card"
```

**Example 3: Branch Location Extraction**
```
User: "Find branch in New York"
Intent: branch_locator
Entities:
  - branch_location: "New York"
```

**Example 4: Account Number Extraction**
```
User: "My account number is 123456789"
Intent: provide_verification
Entities:
  - account_number: "123456789"
```

---

## 6. Dialogue Management

### 6.1 Conversation State (Slots)

The chatbot maintains conversation state through **slots**:

| Slot | Type | Purpose | Initial Value |
|------|------|---------|---------------|
| `account_type` | Text | Current account type in context | None |
| `card_type` | Text | Current card type in context | None |
| `identity_verified` | Boolean | Flag for verified identity | `false` |
| `requested_action` | Text | Action pending verification | None |
| `verification_attempts` | Float | Count of failed verification attempts | `0.0` |
| `branch_location` | Text | Location for branch search | None |

### 6.2 Dialogue Policies

The chatbot uses the following dialogue management policies:

1. **MemoizationPolicy** - Remembers exact conversation patterns
2. **RulePolicy** - Handles specific rules (greet, goodbye, handoff, fallback)
3. **UnexpecTEDIntentPolicy** - Handles unexpected intents
4. **TEDPolicy** (Transformer Embedding Dialogue) - Main dialogue policy
   - Max history: 5 turns
   - Epochs: 100

### 6.3 Conversation Flows (Stories)

#### **Flow 1: Balance Check with Verification**

```
User: "Hello"
Bot: [utter_greet] "Hello! I'm your bank's virtual assistant..."

User: "What's my balance?"
Bot: [action_check_balance] 
     "For security purposes, I need to verify your identity..."

User: "123456789"
Bot: [action_verify_identity] 
     "Identity verified. Your checking account balance is $5,432.10..."
```

**Story Definition:**
```yaml
- story: happy path balance check
  steps:
    - intent: greet
    - action: utter_greet
    - intent: check_balance
    - action: action_check_balance
    - intent: provide_verification
    - action: action_verify_identity
```

#### **Flow 2: Lost Card Assistance**

```
User: "I lost my credit card"
Bot: [action_lost_card_flow]
     "I'm sorry to hear that your credit card has been lost or stolen..."
     "Here are the steps to secure your account:
      1. Freeze your card immediately...
      2. Report the incident...
      3. Request a replacement card...
      4. Monitor your account...
      
      Would you like me to connect you with a human agent?"

User: "Yes"
Bot: [utter_human_handoff]
     "I'll connect you with a human agent right away..."
```

**Story Definition:**
```yaml
- story: lost card happy path
  steps:
    - intent: lost_card
      entities:
      - card_type: "credit card"
    - action: action_lost_card_flow
    - intent: affirm
    - action: utter_human_handoff
```

#### **Flow 3: Branch Locator**

```
User: "Where is the nearest branch?"
Bot: [action_branch_locator]
     "The nearest branch is:
      Central Branch
      Address: 789 Bank Avenue, New York, NY 10003
      Phone: (212) 555-0300
      Hours: Mon-Fri: 9:00 AM - 5:00 PM, Sat: 9:00 AM - 2:00 PM"
```

#### **Flow 4: Human Handoff**

```
User: "This isn't helping, I need to talk to someone"
Bot: [utter_human_handoff]
     "I'll connect you with a human agent right away. One moment please..."
```

**Rule Definition:**
```yaml
- rule: Always handoff to human when explicitly requested
  steps:
    - intent: request_human
    - action: utter_human_handoff
```

### 6.4 Rules

Rules handle specific patterns that should always execute the same way:

1. **Greet Rule** - Always greet when user says hello
2. **Goodbye Rule** - Always say goodbye when user says goodbye
3. **Human Handoff Rule** - Always handoff when user explicitly requests
4. **Fallback Rules** - Handle unknown queries with fallback handler

---

## 7. Custom Actions

### 7.1 Action Overview

Custom actions are Python functions that execute business logic and connect to backend systems.

| Action | Purpose | Verification Required |
|--------|---------|----------------------|
| `action_check_balance` | Retrieve and display account balance | Yes |
| `action_view_transactions` | Retrieve and display recent transactions | Yes |
| `action_branch_locator` | Find and display branch locations | No |
| `action_verify_identity` | Verify user identity via account number | N/A |
| `action_lost_card_flow` | Guide user through lost card process | No |
| `action_general_faq` | Answer general banking questions | No |
| `action_fallback_handler` | Handle unknown queries | No |
| `action_set_identity_verified` | Set identity verification flag | N/A |

### 7.2 Action Details

#### **Action: `action_check_balance`**

**Purpose:** Retrieve and display account balance

**Workflow:**
1. Check if `identity_verified` slot is `True`
2. If not verified:
   - Request verification
   - Set `requested_action` slot to "check_balance"
   - Return (wait for verification)
3. If verified:
   - Get `account_type` from slot (default: "checking")
   - Query backend for balance (currently mocked)
   - Format and return balance

**Backend Integration:**
```python
# Mocked implementation
mock_balances = {
    "checking": "$5,432.10",
    "savings": "$12,345.67",
    "default": "$5,432.10"
}
balance = mock_balances.get(account_type.lower(), mock_balances["default"])
```

**Production Implementation:**
```python
# Real implementation would call:
response = requests.get(
    f"{ACCOUNT_API_URL}/accounts/{account_id}/balance",
    headers={"Authorization": f"Bearer {token}"}
)
balance = response.json()["balance"]
```

#### **Action: `action_view_transactions`**

**Purpose:** Retrieve and display recent transactions

**Workflow:**
1. Check if `identity_verified` slot is `True`
2. If not verified:
   - Request verification
   - Set `requested_action` slot to "view_transactions"
   - Return (wait for verification)
3. If verified:
   - Query backend for recent transactions (currently mocked)
   - Format transactions list
   - Return formatted response

**Mocked Transaction Data:**
```python
mock_transactions = [
    {"date": "2024-11-19", "description": "DEBIT CARD PURCHASE - COFFEE SHOP", "amount": "-$4.50"},
    {"date": "2024-11-19", "description": "DIRECT DEPOSIT - SALARY", "amount": "+$3,500.00"},
    {"date": "2024-11-18", "description": "ONLINE BILL PAY - UTILITIES", "amount": "-$125.00"},
    # ... more transactions
]
```

#### **Action: `action_branch_locator`**

**Purpose:** Find and display branch locations

**Workflow:**
1. Extract `branch_location` from entities or slot
2. Query branch service for matching branches (currently mocked)
3. Format branch details (name, address, phone, hours)
4. Return formatted response

**No Verification Required** - Public information

**Mocked Branch Data:**
```python
mock_branches = {
    "new york": {
        "name": "Main Street Branch",
        "address": "123 Main Street, New York, NY 10001",
        "phone": "(212) 555-0100",
        "hours": "Mon-Fri: 9:00 AM - 5:00 PM, Sat: 9:00 AM - 2:00 PM"
    },
    "downtown": {...},
    "default": {...}
}
```

#### **Action: `action_verify_identity`**

**Purpose:** Verify user identity before allowing access to sensitive information

**Workflow:**
1. Extract account number from entities or message text
2. Validate account number format (6+ digits for demo)
3. If valid and `requested_action` is set:
   - Complete the requested action automatically (balance/transactions)
   - Set `identity_verified` to `True`
   - Clear `requested_action`
   - Return results
4. If valid but no pending action:
   - Set `identity_verified` to `True`
   - Confirm verification
5. If invalid:
   - Increment `verification_attempts`
   - If attempts >= 3: Offer human handoff
   - Otherwise: Request valid account number

**Security Features:**
- Rate limiting: Maximum 3 attempts
- Automatic escalation after failed attempts
- Account number format validation

**Production Implementation:**
```python
# Real implementation would call:
response = requests.post(
    f"{IDENTITY_API_URL}/verify",
    json={"account_number": account_number},
    headers={"Authorization": f"Bearer {token}"}
)
verified = response.json()["verified"]
```

#### **Action: `action_lost_card_flow`**

**Purpose:** Guide user through lost/stolen card process

**Workflow:**
1. Check if there's a pending verification request (redirect if needed)
2. Extract card type from entities or slot
3. Display empathy message
4. Provide step-by-step instructions:
   - Freeze card immediately
   - Report incident
   - Request replacement
   - Monitor account
5. Offer human agent handoff

**Security Note:** Bot **does NOT** perform the action directly - only provides guidance

#### **Action: `action_general_faq`**

**Purpose:** Answer general banking questions

**Workflow:**
1. Extract keywords from user query
2. Match against FAQ knowledge base (currently keyword-based)
3. Return relevant answer
4. If no match: Return general helpful message

**No Verification Required** - Public information

#### **Action: `action_fallback_handler`**

**Purpose:** Handle unknown or unrecognized queries

**Workflow:**
1. Display helpful message acknowledging uncertainty
2. List available services
3. Offer human agent handoff

**Triggered by:**
- `nlu_fallback` intent (low confidence from FallbackClassifier)
- `unknown_query` intent

---

## 8. Backend Integration

### 8.1 Current Implementation (Mocked)

The chatbot currently uses **mocked data** for demonstration purposes. All backend calls are simulated.

### 8.2 Backend Services Architecture

#### **8.2.1 Account Service**

**Endpoints:**

1. **Get Account Balance**
   ```
   GET /api/v1/accounts/{accountId}/balance
   Authorization: Bearer {token}
   
   Response:
   {
     "account_id": "123456789",
     "account_type": "checking",
     "balance": 5432.10,
     "currency": "USD",
     "last_updated": "2024-11-20T12:00:00Z"
   }
   ```

2. **Get Recent Transactions**
   ```
   GET /api/v1/accounts/{accountId}/transactions?limit=10
   Authorization: Bearer {token}
   
   Response:
   {
     "account_id": "123456789",
     "transactions": [
       {
         "date": "2024-11-19",
         "description": "DEBIT CARD PURCHASE - COFFEE SHOP",
         "amount": -4.50,
         "type": "debit"
       },
       {
         "date": "2024-11-19",
         "description": "DIRECT DEPOSIT - SALARY",
         "amount": 3500.00,
         "type": "credit"
       }
       // ... more transactions
     ]
   }
   ```

3. **Verify Identity**
   ```
   POST /api/v1/identity/verify
   Authorization: Bearer {token}
   Content-Type: application/json
   
   Request:
   {
     "account_number": "123456789",
     "additional_info": {...}
   }
   
   Response:
   {
     "verified": true,
     "account_id": "123456789",
     "customer_id": "CUST12345",
     "timestamp": "2024-11-20T12:00:00Z"
   }
   ```

#### **8.2.2 Branch Service**

**Endpoints:**

1. **Find Branches**
   ```
   GET /api/v1/branches?location={location}&radius={radius}
   
   Response:
   {
     "branches": [
       {
         "branch_id": "BR001",
         "name": "Main Street Branch",
         "address": {
           "street": "123 Main Street",
           "city": "New York",
           "state": "NY",
           "zip": "10001"
         },
         "phone": "(212) 555-0100",
         "hours": {
           "weekdays": "9:00 AM - 5:00 PM",
           "saturday": "9:00 AM - 2:00 PM",
           "sunday": "Closed"
         },
         "distance": 0.5,
         "coordinates": {
           "lat": 40.7128,
           "lon": -74.0060
         }
       }
       // ... more branches
     ]
   }
   ```

2. **Get Branch Details**
   ```
   GET /api/v1/branches/{branchId}
   
   Response:
   {
     "branch_id": "BR001",
     "name": "Main Street Branch",
     // ... full branch details
   }
   ```

#### **8.2.3 Card Service**

**Endpoints:**

1. **Get Card Status** (Not directly called by bot)
   ```
   GET /api/v1/cards/{cardId}/status
   Authorization: Bearer {token}
   
   Response:
   {
     "card_id": "CARD123",
     "status": "active",
     "card_type": "credit",
     "last_updated": "2024-11-20T12:00:00Z"
   }
   ```

2. **Freeze Card** (Not called by bot - for security)
   ```
   POST /api/v1/cards/{cardId}/freeze
   Authorization: Bearer {token}
   
   Response:
   {
     "card_id": "CARD123",
     "status": "frozen",
     "timestamp": "2024-11-20T12:00:00Z"
   }
   ```

**Note:** The bot does NOT call this endpoint directly. It provides instructions for the user to freeze their card through other channels (mobile app, online banking, phone).

### 8.3 Integration Pattern

#### **Current Action Implementation Pattern:**

```python
class ActionCheckBalance(Action):
    def run(self, dispatcher, tracker, domain):
        # 1. Security check
        if not tracker.get_slot("identity_verified"):
            return [SlotSet("requested_action", "check_balance")]
        
        # 2. Get parameters
        account_type = tracker.get_slot("account_type") or "checking"
        account_id = tracker.get_slot("account_id")  # Would be set during verification
        
        # 3. Call backend API (currently mocked)
        # response = requests.get(
        #     f"{API_URL}/accounts/{account_id}/balance",
        #     headers={"Authorization": f"Bearer {token}"}
        # )
        # balance = response.json()["balance"]
        
        # 4. Mock implementation
        balance = "$5,432.10"
        
        # 5. Format response
        dispatcher.utter_message(
            text=f"Your {account_type} account balance is {balance}."
        )
        
        return []
```

#### **Production Integration Requirements:**

1. **Authentication:**
   - OAuth 2.0 tokens
   - Service-to-service authentication
   - Token refresh mechanism

2. **Error Handling:**
   - Network timeout handling
   - Retry logic with exponential backoff
   - Graceful degradation

3. **Data Encryption:**
   - HTTPS/TLS for all API calls
   - Encrypted request/response payloads
   - Secure credential storage

4. **Monitoring:**
   - API call logging
   - Performance metrics
   - Error tracking

### 8.4 Data Flow Examples

#### **Example 1: Balance Check Flow**

```
1. User: "What's my balance?"
   └─> Rasa NLU: Classifies as `check_balance` intent
   
2. Rasa Core: Triggers `action_check_balance`
   └─> Action: Checks `identity_verified` slot (False)
   └─> Action: Sets `requested_action` = "check_balance"
   └─> Action: Requests verification
   
3. User: "123456789"
   └─> Rasa NLU: Classifies as `provide_verification` intent
   └─> Rasa NLU: Extracts `account_number` entity = "123456789"
   
4. Rasa Core: Triggers `action_verify_identity`
   └─> Action: Calls Identity Service API
   │   POST /api/v1/identity/verify
   │   { "account_number": "123456789" }
   └─> Response: { "verified": true, "account_id": "123456789" }
   
5. Action: Sets `identity_verified` = True
   Action: Detects `requested_action` = "check_balance"
   Action: Calls Account Service API
   │   GET /api/v1/accounts/123456789/balance
   │   Authorization: Bearer {token}
   └─> Response: { "balance": 5432.10, "currency": "USD" }
   
6. Action: Formats response
   └─> Bot: "Identity verified. Your checking account balance is $5,432.10."
```

#### **Example 2: Branch Locator Flow**

```
1. User: "Find branch in New York"
   └─> Rasa NLU: Classifies as `branch_locator` intent
   └─> Rasa NLU: Extracts `branch_location` entity = "New York"
   
2. Rasa Core: Triggers `action_branch_locator`
   └─> Action: Calls Branch Service API
   │   GET /api/v1/branches?location=New%20York
   └─> Response: { "branches": [...] }
   
3. Action: Formats branch details
   └─> Bot: "The nearest branch is: Main Street Branch..."
```

---

## 9. Security Architecture

### 9.1 Security Layers

#### **Layer 1: Intent-Based Access Control**

| Intent | Verification Required | Sensitive Data |
|--------|----------------------|----------------|
| `check_balance` | ✅ Yes | Account balance |
| `view_transactions` | ✅ Yes | Transaction history |
| `branch_locator` | ❌ No | Public information |
| `general_faq` | ❌ No | Public information |
| `lost_card` | ❌ No | Guidance only |
| `freeze_card` | ❌ No | Instructions only |

#### **Layer 2: Identity Verification System**

**Process:**
1. User requests sensitive information
2. Bot requests account number
3. User provides account number
4. Bot validates format (6+ digits)
5. Bot calls Identity Service API
6. If verified:
   - Set `identity_verified` = True
   - Complete requested action
7. If not verified:
   - Increment `verification_attempts`
   - If attempts >= 3: Offer human handoff
   - Otherwise: Request retry

**Rate Limiting:**
- Maximum 3 verification attempts per session
- Automatic escalation after 3 failures
- Prevents brute force attacks

#### **Layer 3: Action Restrictions**

**Actions Bot CANNOT Perform:**
- ❌ Freeze/cancel cards
- ❌ Transfer money
- ❌ Modify account settings
- ❌ Change passwords
- ❌ Approve loans
- ❌ Open new accounts

**Actions Bot CAN Perform:**
- ✅ Provide information (after verification)
- ✅ Give instructions
- ✅ Answer general questions
- ✅ Connect to human agents

### 9.2 Data Handling

#### **Conversation Data:**
- Sensitive data not stored in conversation logs
- Account numbers not persisted in tracker
- Verification attempts logged for security auditing

#### **API Security:**
- All API calls use HTTPS/TLS
- Bearer token authentication
- Request/response encryption
- Rate limiting on backend

### 9.3 Mocked Security Implementation

**Current Demo Implementation:**
```python
# Simple format validation (for demo only)
if account_number and len(str(account_number)) >= 6:
    # Accept any 6+ digit number as valid
    return True
```

**Production Requirements:**
- Multi-factor authentication (MFA)
- Knowledge-based authentication (KBA)
- Biometric verification (voice/fingerprint)
- Secure API integration with encryption
- Fraud detection algorithms
- Audit logging

---

## 10. Human Handoff Mechanism

### 10.1 Handoff Triggers

The chatbot automatically offers or performs human handoff in the following scenarios:

#### **1. Explicit User Request**

**Trigger Intent:** `request_human`

**Recognized Phrases:**
- "I want to talk to a human"
- "This isn't helping"
- "I need to speak with someone"
- "Connect me to an agent"
- "This bot isn't helping"

**Response:**
```
Bot: "I'll connect you with a human agent right away. One moment please..."
```

#### **2. Failed Identity Verification**

**Trigger:** `verification_attempts >= 3`

**Response:**
```
Bot: "I'm sorry, I couldn't verify your identity after multiple attempts. 
      For your security, I can only provide general information. 
      Would you like to speak with a human agent?"
```

#### **3. Security-Sensitive Requests**

**Trigger:** User requests actions bot cannot perform (e.g., "freeze my card")

**Response:**
```
Bot: "For security reasons, I cannot freeze your card directly through this chat. 
      Would you like to speak with a human agent who can assist you immediately?"
```

### 10.2 Handoff Process

#### **Current Implementation (Mocked):**

1. Bot acknowledges request
2. Bot apologizes for inability to help
3. Bot offers immediate connection
4. Bot displays handoff message

#### **Production Implementation:**

1. **Context Transfer:**
   ```python
   handoff_context = {
       "conversation_id": tracker.sender_id,
       "conversation_history": tracker.events,
       "slots": tracker.current_slot_values(),
       "last_intent": tracker.latest_message.get("intent"),
       "priority": calculate_priority(tracker)  # Urgent for lost card
   }
   ```

2. **Agent Queue:**
   ```python
   agent_queue.add(
       conversation_id=tracker.sender_id,
       context=handoff_context,
       priority=priority_level,
       timestamp=datetime.now()
   )
   ```

3. **Agent Assignment:**
   - Route to available agent
   - Priority queue (urgent issues first)
   - Skill-based routing (card issues → card specialist)

4. **Session Continuity:**
   - Transfer conversation history
   - Maintain slot values
   - Provide agent with full context

### 10.3 Handoff Priority Levels

| Priority | Scenario | Response Time |
|----------|----------|---------------|
| **Urgent** | Lost/stolen card | Immediate |
| **High** | Failed verification | < 1 minute |
| **Medium** | Explicit request | < 2 minutes |
| **Low** | General inquiry | Standard queue |

---

## 11. NLP: Recognizing Variations

### 11.1 Semantic Variations

The chatbot recognizes **semantic variations** through the DIET classifier's word embeddings and training data.

#### **Example: Lost Card Variations**

All of these trigger the `lost_card` intent:
- "I lost my card"
- "Card got stolen"
- "My card was stolen"
- "Someone stole my card"
- "My card is missing"
- "Card disappeared"

**How it works:**
1. Training data includes multiple variations
2. DIET classifier learns word embeddings
3. Similar meanings map to same intent
4. Context-aware classification

#### **Example: Balance Query Variations**

All of these trigger the `check_balance` intent:
- "What's my balance?"
- "Check my account balance"
- "How much money do I have?"
- "Show me my balance"

### 11.2 Entity Variations

#### **Account Type Recognition:**
- "savings account" → `account_type: "savings"`
- "checking" → `account_type: "checking"`
- "checking account" → `account_type: "checking"`

#### **Card Type Recognition:**
- "credit card" → `card_type: "credit card"`
- "debit card" → `card_type: "debit card"`
- "my card" → `card_type: None` (defaults to "card")

---

## 12. Deployment Architecture

### 12.1 Development Environment

```
┌─────────────┐
│   User      │
│  (Terminal) │
└──────┬──────┘
       │
       ▼
┌──────────────────┐
│  Rasa Shell      │
│  (Interactive)   │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Rasa Core       │
│  (localhost:5005)│
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│  Action Server   │
│  (localhost:5055)│
└──────────────────┘
```

### 12.2 Production Architecture

```
┌─────────────┐
│   User      │
│  (Web/Mobile)│
└──────┬──────┘
       │ HTTPS
       ▼
┌──────────────────┐
│  Load Balancer   │
└──────┬───────────┘
       │
   ┌───┴───┐
   ▼       ▼
┌──────┐ ┌──────┐
│Rasa  │ │Rasa  │
│Server│ │Server│
└───┬──┘ └───┬──┘
    │        │
    └───┬────┘
        │
        ▼
┌──────────────────┐
│  Action Server   │
│  (Kubernetes)    │
└──────┬───────────┘
       │
   ┌───┴───┐
   ▼       ▼
┌──────┐ ┌──────┐
│Account│ │Branch│
│Service│ │Service│
└──────┘ └──────┘
```

### 12.3 Scalability Considerations

- **Horizontal Scaling:** Multiple Rasa Core instances behind load balancer
- **Action Server:** Stateless design allows multiple instances
- **Database:** Shared tracker store (Redis/PostgreSQL)
- **Caching:** Cache frequent queries (branch locations, FAQs)
- **Monitoring:** Logging, metrics, error tracking

---

## 13. Future Enhancements

### 13.1 Planned Features

1. **Voice Interface:** Integration with voice assistants
2. **Multi-language Support:** Support for multiple languages
3. **Sentiment Analysis:** Detect user frustration for automatic handoff
4. **Proactive Messaging:** Notify users about suspicious activity
5. **Knowledge Base Integration:** Connect to comprehensive FAQ database
6. **Voice Biometrics:** Enhanced identity verification

### 13.2 GPT-Based Fallback (Optional)

A GPT-based component can be integrated for unknown queries with proper guardrails:

**Guardrails Required:**
- System prompt restrictions
- Output filtering
- Rate limiting
- Context filtering
- Cost monitoring

**Risks Without Guardrails:**
- Data leakage
- Unauthorized actions
- Hallucinations
- Context bleeding
- High costs

---

## Appendix A: File Structure

```
Customer_Support_Chatbot/
├── actions/
│   ├── __init__.py
│   └── actions.py          # Custom action implementations
├── data/
│   ├── nlu.yml            # Intent training data with sample utterances
│   ├── stories.yml        # Conversation flows
│   └── rules.yml          # Conversation rules
├── docs/
│   └── CHATBOT_ARCHITECTURE.md  # This document
├── config.yml             # Rasa configuration (NLU pipeline, policies)
├── domain.yml             # Domain definition (intents, entities, responses, actions)
├── credentials.yml        # API credentials configuration
├── endpoints.yml          # Action server and tracker store endpoints
├── requirements.txt       # Python dependencies
└── README.md             # Project documentation
```

---

## Appendix B: Training Data Statistics

- **Total Intents:** 14
- **Total Training Examples:** ~150+ utterances
- **Total Entities:** 6
- **Total Stories:** 15+
- **Total Rules:** 5
- **Custom Actions:** 8

---

## Document Version

- **Version:** 1.0
- **Last Updated:** November 2024
- **Author:** Bank Customer Service Chatbot Team

---

**End of Architecture Documentation**

