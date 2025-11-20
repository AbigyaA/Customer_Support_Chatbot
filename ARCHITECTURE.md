# Chatbot Architecture Documentation

## System Overview

This document describes the architecture of the Bank Customer Service Chatbot, focusing on intent recognition, dialogue flow, human handoff mechanisms, and security measures.

## 1. Intent Recognition & NLP Pipeline

### NLU Pipeline Components

The chatbot uses Rasa's default NLU pipeline with the following components:

1. **WhitespaceTokenizer**: Tokenizes input text into words
2. **LexicalSyntacticFeaturizer**: Creates lexical and syntactic features
3. **CountVectorsFeaturizer**: Creates bag-of-words features
4. **DIETClassifier**: Dual Intent and Entity Transformer for intent classification and entity extraction
5. **EntitySynonymMapper**: Maps entities to canonical forms
6. **ResponseSelector**: Selects appropriate responses
7. **FallbackClassifier**: Detects low-confidence predictions

### Intent Categories

#### Account Management Intents
- `check_balance`: Query account balance
- `view_transactions`: View transaction history

#### Service Intents
- `branch_locator`: Find branch locations
- `general_faq`: General banking questions

#### Incident Management Intents
- `lost_card`: Report lost/stolen card
- `freeze_card`: Request card freeze

#### Meta Intents
- `greet`, `goodbye`: Social pleasantries
- `affirm`, `deny`: Confirmation responses
- `request_human`: Escalation request
- `verify_identity`: Provide verification information
- `provide_verification`: User provides account number for verification
- `unknown_query`: Fallback for unrecognized input
- `nlu_fallback`: Automatically triggered by FallbackClassifier when confidence is low (< 0.3)

### Sample Utterances & Variations

The chatbot recognizes semantic variations through training data:

**Lost Card Variations:**
- "I lost my card"
- "My card was stolen"
- "Card got stolen"
- "Someone stole my credit card"
- "My debit card is missing"

All these trigger the `lost_card` intent because:
1. They share semantic meaning (loss/theft of card)
2. DIET classifier learns word embeddings and context
3. Training data includes multiple variations

**Balance Query Variations:**
- "What's my balance?"
- "Check my account balance"
- "How much money do I have?"
- "Show me my balance"

All trigger `check_balance` intent.

### Entity Extraction

Entities are extracted from user input:
- `account_type`: "savings", "checking"
- `card_type`: "credit card", "debit card"
- `branch_location`: Location names or addresses
- `account_number`: Numeric identifiers (6+ digits)

## 2. Dialogue Flow & Stories

### Story Architecture

Stories define conversation flows:

1. **Linear Stories**: Simple sequential flows
   - Example: Greet → Check Balance → Verify → Show Balance → Goodbye

2. **Branching Stories**: Multiple paths based on user choice
   - Example: Lost Card → Empathy → Steps → [Yes/No to Handoff]

3. **Conditional Stories**: Flow depends on slot values
   - Example: Check Balance → [Has Account Type / No Account Type] → Verify

### Key Conversation Patterns

#### Pattern 1: Identity-Protected Information Flow
```
User: Check Balance
Bot: Request Verification
User: Provide Account Number
Bot: Verify Identity
Bot: Show Balance (if verified)
Bot: Request Human (if verification fails)
```

#### Pattern 2: Lost Card Incident Flow
```
User: Report Lost Card
Bot: Empathy Message
Bot: Provide Steps (no direct action)
Bot: Offer Human Handoff
User: [Accept/Deny]
Bot: [Connect to Human / End]
```

#### Pattern 3: Public Information Flow
```
User: Find Branch
Bot: Ask Location (optional)
Bot: Show Branch Info
Bot: Offer Additional Help
```

## 3. Human Agent Handoff Mechanism

### Handoff Triggers

#### 1. Explicit User Request
**Intent**: `request_human`

**Recognized Variations:**
- "I want to talk to a human"
- "This isn't helping"
- "I need to speak with someone"
- "Connect me to an agent"
- "This bot isn't helping"

**Implementation:**
- Rule in `rules.yml` ensures immediate handoff
- No questions asked, direct connection offered
- Response: `utter_human_handoff`

#### 2. Failed Identity Verification
**Trigger**: `verification_attempts >= 3`

**Flow:**
1. User attempts verification multiple times
2. Bot tracks attempts in `verification_attempts` slot
3. After 3 failed attempts, automatic handoff offered
4. Security measure prevents brute force attempts

**Implementation:**
```python
if verification_attempts >= 3:
    dispatcher.utter_message(
        "I'm sorry, I couldn't verify your identity after multiple attempts. "
        "For your security, I can only provide general information. "
        "Would you like to speak with a human agent?"
    )
```

#### 3. Security-Related Requests
**Trigger**: Sensitive actions that bot cannot perform

**Examples:**
- Direct card freeze requests
- Account modifications
- Large transfers
- Dispute handling

**Response**: Provide steps and offer immediate handoff

### Handoff Process

1. **Acknowledgment**: Bot acknowledges user request/need
2. **Apology**: Expresses regret for inability to help
3. **Transfer**: Offers immediate connection
4. **Context Transfer**: (In production) Transfers conversation context to agent

**Example:**
```
User: "This isn't helping, I need to talk to someone"

Bot: "I'll connect you with a human agent right away. One moment please..."
```

### Production Handoff Implementation

In a production system, handoff would involve:

1. **Agent Queue System**: Route to available agent
2. **Context Transfer**: Send conversation history
3. **Session Management**: Maintain continuity
4. **Priority Routing**: Urgent issues (lost card) get priority
5. **Callback Option**: Offer callback if queue is long

**Pseudocode:**
```python
class ActionHumanHandoff(Action):
    def run(self, dispatcher, tracker, domain):
        # Transfer to agent queue
        conversation_id = tracker.sender_id
        context = {
            "conversation": tracker.events,
            "slots": tracker.current_slot_values(),
            "intent": tracker.latest_message.get("intent"),
            "priority": self._calculate_priority(tracker)
        }
        
        agent_queue.add(conversation_id, context)
        dispatcher.utter_message("Connecting you with an agent...")
```

## 4. Security Measures

### Identity Verification System

#### Purpose
Prevent unauthorized access to account information.

#### Method
**Account Number Verification** (Mocked in demo)

**Production Implementation Would Use:**
- Multi-factor authentication (MFA)
- Knowledge-based authentication (KBA)
- Biometric verification (voice/fingerprint)
- SMS/Email verification codes
- Two-factor authentication (2FA)

#### Current Implementation
```python
def verify_identity(account_number, requested_action):
    # Mocked: Accepts 6+ digit numbers
    if len(str(account_number)) >= 6:
        if requested_action == "check_balance":
            # Automatically complete balance check
            return show_balance()
        elif requested_action == "view_transactions":
            # Automatically show transactions
            return show_transactions()
        return True
    return False
```

**Limitations:**
- Very basic validation
- No real database check
- No MFA

**Production Requirements:**
- Secure API connection (HTTPS/TLS)
- Encrypted storage
- Rate limiting
- Fraud detection
- Audit logging

### Information Access Control

#### Tier 1: Public Information (No Verification)
- Branch locations and hours
- General banking FAQs
- Service descriptions
- Interest rate information (general)

#### Tier 2: Identity Verification Required
- Account balance
- Transaction history
- Account status
- Card information

#### Tier 3: Human Agent Only
- Card freeze/cancel
- Account modifications
- Transfer authorizations
- Dispute handling
- Password resets

### Slot-Based Security

**Security Slots:**
- `identity_verified`: Boolean flag (default: False, type: bool)
- `verification_attempts`: Counter (max: 3, type: float, initial: 0.0)
- `requested_action`: Action pending verification (type: text)

**Slot Flow:**
```
User requests sensitive info
→ Set requested_action slot (e.g., "check_balance")
→ Request verification
→ User provides account number
→ Verify identity
→ Set identity_verified = True
→ Automatically complete requested_action (balance/transactions shown immediately)
→ Clear requested_action slot
```

### Conversation Security

#### Data Handling
- **No Storage**: Sensitive data not stored in conversation logs
- **Encryption**: All data encrypted in transit (HTTPS)
- **Session Timeout**: Sessions expire after inactivity
- **Audit Trail**: All verification attempts logged

#### Guardrails

**1. Cannot Perform Actions**
- Bot cannot freeze cards
- Bot cannot transfer money
- Bot cannot modify accounts
- Bot provides instructions only

**2. Limited Information**
- Only provides information after verification
- Cannot access other accounts
- Cannot view full account numbers

**3. Rate Limiting**
- Maximum 3 verification attempts
- Prevents brute force attacks
- Temporary lockout after failures

### Mocked Backend Security

**Current Implementation:**
- All data is mocked
- Verification is simulated
- No real database connections

**Production Requirements:**

```python
# Production API call example
import requests
from cryptography.fernet import Fernet

def verify_identity(account_number, additional_info):
    # Encrypt request
    encrypted_data = encrypt(account_number, additional_info)
    
    # Secure API call
    response = requests.post(
        "https://api.bank.com/identity/verify",
        json=encrypted_data,
        headers={
            "Authorization": "Bearer {token}",
            "Content-Type": "application/json"
        },
        timeout=5
    )
    
    # Verify response signature
    if verify_signature(response):
        return response.json()["verified"]
    
    return False
```

## 5. Backend System Integration

### System Architecture Diagram

```
┌─────────────┐
│   User      │
│  (Chat UI)  │
└──────┬──────┘
       │ HTTP/REST
       ▼
┌─────────────────────────────────────┐
│         Rasa Core Server            │
│  ┌──────────┐      ┌──────────────┐ │
│  │   NLU    │─────▶│   Dialogue   │ │
│  │ (DIET)   │      │  Management  │ │
│  └──────────┘      └──────┬───────┘ │
└───────────────────────────┼─────────┘
                            │
                            ▼
                   ┌─────────────────┐
                   │  Action Server  │
                   │  (Custom Actions)│
                   └────────┬────────┘
                            │
            ┌───────────────┼───────────────┐
            │               │               │
            ▼               ▼               ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐
    │ Account  │   │  Branch  │   │   FAQ    │
    │ Service  │   │ Service  │   │ Knowledge│
    │   API    │   │   API    │   │   Base   │
    └──────────┘   └──────────┘   └──────────┘
```

### API Endpoints (Mocked)

#### Account Service
```
GET /api/v1/accounts/{accountId}/balance
GET /api/v1/accounts/{accountId}/transactions
POST /api/v1/identity/verify
```

#### Branch Service
```
GET /api/v1/branches?location={location}
GET /api/v1/branches/{branchId}
```

#### Card Service
```
GET /api/v1/cards/{cardId}/status
POST /api/v1/cards/{cardId}/freeze  (Not called by bot)
```

### Data Flow Examples

#### Balance Check Flow
```
1. User: "Check my balance"
2. Rasa NLU: Classifies as check_balance intent
3. Rasa Core: Triggers action_check_balance
4. Action Server: Checks identity_verified slot
5. If not verified: 
   - Set requested_action = "check_balance"
   - Request verification (dispatcher.utter_message)
6. User: Provides account number (e.g., "123456789")
7. Rasa NLU: Classifies as provide_verification intent
8. Rasa Core: Triggers action_verify_identity
9. Action Server: Verifies identity (mocked validation)
10. If verified:
    - Set identity_verified = True
    - Check requested_action slot
    - Automatically complete balance check (no need to re-trigger)
    - Format and return balance directly: "Identity verified. Your checking account balance is $5,432.10."
    - Clear requested_action slot
11. User receives balance immediately without repeating request
```

#### Branch Locator Flow
```
1. User: "Find branch in New York"
2. Rasa NLU: Extracts branch_location entity = "New York"
3. Rasa Core: Triggers action_branch_locator
4. Action Server: Calls Branch Service API
5. API Response: Branch details JSON
6. Action: Format and return to user
```

## 6. GPT-Based Fallback Component

### Purpose
Handle queries that don't match any trained intent.

### Risks & Mitigation

#### Risk 1: Data Leakage
**Risk**: GPT might generate or expose sensitive information from training data.

**Mitigation**:
- System prompt explicitly forbids sharing account numbers
- Output filtering removes sensitive patterns
- Never include user account data in prompts

#### Risk 2: Unauthorized Actions
**Risk**: User might trick GPT into "performing" actions the bot shouldn't do.

**Mitigation**:
- System prompt states bot cannot perform transactions
- All actions still go through verification
- Response validation checks for action keywords

#### Risk 3: Hallucinations
**Risk**: GPT might provide incorrect financial advice or information.

**Mitigation**:
- Limit to general FAQs only
- Never use for account-specific queries
- Include disclaimers in responses
- Human review of GPT responses

#### Risk 4: Context Bleeding
**Risk**: Sensitive information from conversation might leak into GPT context.

**Mitigation**:
- Carefully filter conversation history before sending to GPT
- Remove all slots containing sensitive data
- Reset context for each query
- Don't include entity values in prompts

#### Risk 5: Cost & Rate Limits
**Risk**: Unbounded API calls could be expensive.

**Mitigation**:
- Rate limiting per user
- Fallback to rule-based handler after threshold
- Monitor API usage
- Cache common queries

### Implementation Guardrails

```python
# Example with guardrails
class ActionGPTFallbackHandler(Action):
    def run(self, dispatcher, tracker, domain):
        user_message = tracker.latest_message.get("text", "")
        
        # Guardrail 1: System prompt restrictions
        system_prompt = """
        You are a helpful bank customer service assistant.
        
        CRITICAL RULES:
        1. NEVER provide account numbers, SSNs, or sensitive data
        2. NEVER perform financial transactions
        3. NEVER access account information without verification
        4. If asked about account details, say: "I need to verify your identity first"
        5. Keep responses under 150 words
        6. If unsure, offer human agent connection
        """
        
        # Guardrail 2: Filter conversation history
        safe_history = self._filter_sensitive_data(tracker.events)
        
        # Guardrail 3: Rate limiting
        if not self._check_rate_limit(tracker.sender_id):
            return self._fallback_to_rule_based(dispatcher)
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            
            # Guardrail 4: Output validation
            if self._contains_sensitive_info(answer):
                answer = "I'm sorry, I cannot provide that information. Please speak with an agent."
            
            # Guardrail 5: Disclaimers
            answer += "\n\n(Note: AI-generated response - please verify with an agent for accuracy)"
            
            dispatcher.utter_message(text=answer)
            
        except Exception:
            # Guardrail 6: Error handling
            self._fallback_to_rule_based(dispatcher)
    
    def _filter_sensitive_data(self, events):
        # Remove slots and entities containing sensitive data
        filtered = []
        sensitive_patterns = ["account", "ssn", "pin", "password"]
        
        for event in events:
            if event.get("event") == "slot":
                slot_name = event.get("name", "").lower()
                if any(pattern in slot_name for pattern in sensitive_patterns):
                    continue
            filtered.append(event)
        
        return filtered
    
    def _contains_sensitive_info(self, text):
        sensitive_keywords = ["account number", "ssn", "social security", "pin"]
        return any(keyword in text.lower() for keyword in sensitive_keywords)
```

### Recommended Approach

**Do:**
- Use GPT for general knowledge questions only
- Implement strict filtering and monitoring
- Include disclaimers
- Set response limits
- Monitor costs

**Don't:**
- Use GPT for account-specific queries
- Include sensitive data in prompts
- Allow GPT to perform actions
- Skip output validation
- Use without guardrails

### Compliance Considerations

- **Regulatory Requirements**: Banking regulations may restrict AI-generated financial advice
- **Audit Trail**: All GPT interactions must be logged
- **User Consent**: Users should be informed AI is used
- **Accuracy Guarantees**: Disclaimers required for AI responses

## 7. Testing & Validation

### Intent Recognition Testing

Test variations are recognized correctly:
- "I lost my card" → `lost_card`
- "Card got stolen" → `lost_card`
- "My card was taken" → `lost_card`

### Security Testing

- Verify that balance cannot be accessed without verification
- Verify that failed verification triggers handoff
- Verify that sensitive actions are not performed
- Verify rate limiting works

### Dialogue Flow Testing

- Test complete conversation flows
- Test branching scenarios
- Test error handling
- Test handoff triggers

## 8. Monitoring & Analytics

### Key Metrics

1. **Intent Recognition Accuracy**: % of correct intent classifications
2. **Handoff Rate**: % of conversations requiring human agent
3. **Verification Success Rate**: % of successful verifications
4. **User Satisfaction**: Post-conversation surveys
5. **Response Time**: Average time to resolve queries

### Logging

- All verification attempts
- All handoff triggers
- All failed intents (fallback usage)
- All GPT interactions (if enabled)
- Error occurrences

## Conclusion

This architecture prioritizes:
1. **Security**: Multiple layers of protection
2. **User Experience**: Natural dialogue flow
3. **Escalation**: Smooth handoff when needed
4. **Flexibility**: Extensible action system
5. **Safety**: Guardrails for AI components

The system is designed to handle common banking queries while maintaining security and providing appropriate escalation paths.
