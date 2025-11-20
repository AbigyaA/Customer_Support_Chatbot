# Test Queries for Bank Customer Service Chatbot

This document lists all queries you can input as a user to test the chatbot's functionality.

## 📋 Table of Contents
1. [Greetings](#greetings)
2. [Goodbyes](#goodbyes)
3. [Account Balance](#account-balance)
4. [Recent Transactions](#recent-transactions)
5. [Branch Locator](#branch-locator)
6. [Lost/Stolen Card](#loststolen-card)
7. [Freeze Card](#freeze-card)
8. [General FAQs](#general-faqs)
9. [Human Agent Request](#human-agent-request)
10. [Identity Verification](#identity-verification)
11. [Conversation Flow Examples](#conversation-flow-examples)

---

## 1. Greetings

Start your conversation with any of these:

```
hello
hi
hey
good morning
good afternoon
good evening
greetings
hi there
hello there
howdy
```

---

## 2. Goodbyes

End your conversation with:

```
bye
goodbye
see you later
see ya
talk to you later
farewell
have a nice day
thanks bye
bye bye
see you soon
```

---

## 3. Account Balance

**Note**: These require identity verification. The bot will ask for your account number.

### Simple Queries:
```
what's my balance
check my account balance
how much money do i have
show me my balance
what's my account balance
balance check
check balance
i want to see my balance
can you tell me my balance
what is my current balance
```

### With Account Type:
```
check my savings account balance
balance on my checking account
how much is in my savings account
show balance for my checking account
```

**Complete Flow Example:**
```
User: What's my balance?
Bot: [Requests identity verification]
User: My account number is 123456789
Bot: [Shows balance]
```

---

## 4. Recent Transactions

**Note**: These require identity verification.

```
show my recent transactions
what are my recent transactions
transaction history
recent transactions
show transactions
view my transactions
last transactions
transaction list
i want to see my transactions
can you show my transaction history
recent activity
show me recent activity on my account
```

**Complete Flow Example:**
```
User: Show my recent transactions
Bot: [Requests identity verification]
User: 123456789
Bot: [Shows recent transactions]
```

---

## 5. Branch Locator

**Note**: No verification needed - this is public information.

### Simple Queries:
```
find a branch
where is the nearest branch
branch location
locate branch
find branch near me
where's the closest branch
branch locator
show me branches
what branches are nearby
i need to visit a branch
```

### With Location:
```
find branch in New York
nearest branch to downtown
branch near 123 Main St
```

---

## 6. Lost/Stolen Card

**Note**: The bot will provide guidance but cannot perform actions directly.

### Lost Card:
```
i lost my card
my card is lost
i lost my credit card
i lost my debit card
my debit card is missing
i can't find my card
my card disappeared
card is gone
lost my credit card
misplaced my card
card missing
```

### Stolen Card:
```
card got stolen
someone stole my card
my card was stolen
i think my card is stolen
my credit card got stolen
someone took my debit card
my card was taken
```

**Expected Response**: The bot will show empathy, provide step-by-step instructions, and offer to connect you with a human agent.

---

## 7. Freeze Card

**Note**: The bot will provide instructions but cannot freeze your card directly.

```
freeze my card
i want to freeze my card
can you freeze my card
block my card
disable my card
deactivate my card
stop my card
freeze my credit card
block my debit card
i need to freeze my card immediately
suspend my card
cancel my card
```

**Expected Response**: The bot will provide instructions on how to freeze your card and offer to connect you with a human agent.

---

## 8. General FAQs

**Note**: No verification needed for general information.

### Banking Hours:
```
what are your hours
banking hours
when are you open
```

### Services:
```
what services do you offer
tell me about your services
```

### Account Information:
```
how do i open an account
what is the minimum balance
```

### Rates and Fees:
```
interest rates
what are your rates
what are your fees
```

### Transfers and Payments:
```
how do i transfer money
how to pay bills
```

### Password and Settings:
```
how can i change my password
reset password
how do i update my address
```

### Online/Mobile Banking:
```
mobile banking
online banking
what can i do with online banking
```

---

## 9. Human Agent Request

Request to speak with a human agent at any time:

```
i want to talk to a human
can i speak with someone
connect me to an agent
i need a real person
talk to a person
human agent
speak to representative
this isn't helping
this bot isn't helping
i need to talk to someone
can i talk to a human agent
transfer me to a person
connect me with support
i want human assistance
agent please
this isn't working i need help
```

**Expected Response**: The bot will immediately offer to connect you with a human agent.

---

## 10. Identity Verification

When asked for verification, you can provide:

```
my account number is 123456789
account number 987654321
customer id CUST12345
my customer id is CUST67890
here's my account number 111222333
verify with account 444555666
```

Or simply provide the number:
```
123456789
789012
CUST123
345678
901234
```

**Note**: For demo purposes, any 6+ digit number will work. In production, this would verify against a database.

---

## 11. Conversation Flow Examples

### Example 1: Complete Balance Check Flow

```
User: Hello
Bot: Hello! I'm your bank's virtual assistant. How can I help you today?

User: What's my balance?
Bot: For security purposes, I need to verify your identity before accessing 
     account information. Please provide your account number or customer ID.

User: My account number is 123456789
Bot: Identity verified successfully. How can I assist you?
     Your checking account balance is $5,432.10.

User: Thanks, bye
Bot: Thank you for contacting us. Have a great day!
```

### Example 2: Lost Card Flow

```
User: I lost my credit card
Bot: I'm sorry to hear that your credit card has been lost or stolen. 
     This must be stressful. I can help guide you through the steps 
     to protect your account.

Bot: Here are the steps to secure your account:
     1. Freeze your card immediately to prevent unauthorized use
     2. Report the incident through our online portal or mobile app
     3. Request a replacement card
     4. Monitor your account for any suspicious activity

     For security reasons, I cannot freeze your card directly through 
     this chat. Would you like me to connect you with a human agent 
     who can process these actions immediately?

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
```

### Example 4: General FAQ

```
User: What are your hours?
Bot: Our branch hours are Monday-Friday: 9:00 AM - 5:00 PM, 
     Saturday: 9:00 AM - 2:00 PM. Online and mobile banking 
     are available 24/7.
```

### Example 5: Human Handoff

```
User: This isn't helping, I need to talk to someone
Bot: I'll connect you with a human agent right away. 
     One moment please...
```

### Example 6: Transaction History

```
User: Show my recent transactions
Bot: For security purposes, I need to verify your identity before 
     accessing account information. Please provide your account 
     number or customer ID.

User: 123456789
Bot: Identity verified successfully. How can I assist you?
     Here are your recent transactions:

     2024-11-19: DEBIT CARD PURCHASE - COFFEE SHOP -$4.50
     2024-11-19: DIRECT DEPOSIT - SALARY +$3,500.00
     2024-11-18: ONLINE BILL PAY - UTILITIES -$125.00
     2024-11-17: ATM WITHDRAWAL -$100.00
     2024-11-16: TRANSFER FROM SAVINGS +$500.00
```

---

## 🎯 Testing Tips

### Test Variations
The chatbot recognizes semantic variations. Try:
- "I lost my card" vs "Card got stolen" (both trigger lost_card intent)
- "What's my balance?" vs "Check my account balance" (both trigger check_balance)

### Test Security
1. **Try accessing balance without verification** - Bot should request verification
2. **Try multiple failed verifications** - After 3 attempts, bot should offer human handoff
3. **Try requesting sensitive actions** - Bot should provide steps only, not perform actions

### Test Human Handoff
Try these at different points in the conversation:
- "I want to talk to a human"
- "This isn't helping"
- "Connect me to an agent"

### Test Edge Cases
- Unknown queries: Try asking something not in the training data
- Multiple intents: Ask balance, then transactions, then branch locator
- Interruptions: Request human handoff mid-conversation

---

## 📝 Quick Reference

| Intent | Example Query | Verification Required |
|--------|--------------|----------------------|
| greet | "hello" | No |
| check_balance | "what's my balance" | Yes |
| view_transactions | "show my transactions" | Yes |
| branch_locator | "find a branch" | No |
| lost_card | "i lost my card" | No |
| freeze_card | "freeze my card" | No (instructions only) |
| general_faq | "what are your hours" | No |
| request_human | "i want to talk to a human" | No |
| goodbye | "bye" | No |

---

## 🔒 Security Notes

- **Balance & Transactions**: Always require verification (account number)
- **Branch Location**: Public information, no verification needed
- **Lost Card**: Provides guidance only, no direct actions
- **Freeze Card**: Provides instructions only, cannot perform action
- **General FAQs**: Public information, no verification needed

---

**Happy Testing! 🚀**

For more information, see:
- `README.md` - Full project documentation
- `ARCHITECTURE.md` - System architecture details
- `QUICK_START.md` - Quick setup guide

