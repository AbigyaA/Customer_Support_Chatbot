"""
Custom actions for the Bank Customer Service Chatbot
"""

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.types import DomainDict
import random
import json
from datetime import datetime, timedelta


class ActionCheckBalance(Action):
    """Action to check account balance (mocked data)"""

    def name(self) -> Text:
        return "action_check_balance"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # Check if identity is verified
        identity_verified = tracker.get_slot("identity_verified")
        
        if not identity_verified:
            dispatcher.utter_message(
                text="For security purposes, I need to verify your identity before accessing account information. "
                "Please provide your account number or customer ID."
            )
            return [SlotSet("requested_action", "check_balance")]
        
        # If we get here, identity is verified - show balance
        # Get account type from slot or default to checking
        account_type = tracker.get_slot("account_type") or "checking"
        
        # Mock balance data (in real system, this would query a database)
        mock_balances = {
            "checking": "$5,432.10",
            "savings": "$12,345.67",
            "default": "$5,432.10"
        }
        
        balance = mock_balances.get(account_type.lower(), mock_balances["default"])
        
        dispatcher.utter_message(
            text=f"Your {account_type} account balance is {balance}. Is there anything else I can help with?"
        )
        
        return []


class ActionViewTransactions(Action):
    """Action to show recent transactions (mocked data)"""

    def name(self) -> Text:
        return "action_view_transactions"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # Check if identity is verified
        identity_verified = tracker.get_slot("identity_verified")
        
        if not identity_verified:
            dispatcher.utter_message(
                text="For security purposes, I need to verify your identity before accessing account information. "
                "Please provide your account number or customer ID."
            )
            return [SlotSet("requested_action", "view_transactions")]
        
        # If we get here, identity is verified - show transactions

        # Mock transaction data
        today = datetime.now()
        mock_transactions = [
            {"date": (today - timedelta(days=1)).strftime("%Y-%m-%d"), 
             "description": "DEBIT CARD PURCHASE - COFFEE SHOP", 
             "amount": "-$4.50"},
            {"date": (today - timedelta(days=1)).strftime("%Y-%m-%d"), 
             "description": "DIRECT DEPOSIT - SALARY", 
             "amount": "+$3,500.00"},
            {"date": (today - timedelta(days=2)).strftime("%Y-%m-%d"), 
             "description": "ONLINE BILL PAY - UTILITIES", 
             "amount": "-$125.00"},
            {"date": (today - timedelta(days=3)).strftime("%Y-%m-%d"), 
             "description": "ATM WITHDRAWAL", 
             "amount": "-$100.00"},
            {"date": (today - timedelta(days=4)).strftime("%Y-%m-%d"), 
             "description": "TRANSFER FROM SAVINGS", 
             "amount": "+$500.00"},
        ]
        
        transactions_text = "\n".join([
            f"{tx['date']}: {tx['description']} {tx['amount']}"
            for tx in mock_transactions
        ])
        
        dispatcher.utter_message(
            text=f"Here are your recent transactions:\n\n{transactions_text}\n\nIs there anything else you need?"
        )
        
        return []


class ActionBranchLocator(Action):
    """Action to locate nearest branch (mocked data)"""

    def name(self) -> Text:
        return "action_branch_locator"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # Try to get location from entities first
        location = None
        entities = tracker.latest_message.get("entities", [])
        for entity in entities:
            if entity.get("entity") == "branch_location":
                location = entity.get("value")
                break
        
        # If not in entities, try from slot
        if not location:
            location = tracker.get_slot("branch_location")
        
        # Mock branch data
        mock_branches = {
            "new york": {
                "name": "Main Street Branch",
                "address": "123 Main Street, New York, NY 10001",
                "phone": "(212) 555-0100",
                "hours": "Mon-Fri: 9:00 AM - 5:00 PM, Sat: 9:00 AM - 2:00 PM"
            },
            "downtown": {
                "name": "Downtown Branch",
                "address": "456 Market Street, New York, NY 10002",
                "phone": "(212) 555-0200",
                "hours": "Mon-Fri: 8:30 AM - 6:00 PM, Sat: 10:00 AM - 3:00 PM"
            },
            "default": {
                "name": "Central Branch",
                "address": "789 Bank Avenue, New York, NY 10003",
                "phone": "(212) 555-0300",
                "hours": "Mon-Fri: 9:00 AM - 5:00 PM, Sat: 9:00 AM - 2:00 PM"
            }
        }
        
        if location and str(location).lower() in mock_branches:
            branch = mock_branches[str(location).lower()]
        else:
            branch = mock_branches["default"]
        
        branch_details = (
            f"{branch['name']}\n"
            f"Address: {branch['address']}\n"
            f"Phone: {branch['phone']}\n"
            f"Hours: {branch['hours']}"
        )
        
        dispatcher.utter_message(
            text=f"The nearest branch is:\n\n{branch_details}"
        )
        
        return []  # Don't try to set slot to None - just return empty list


class ActionVerifyIdentity(Action):
    """Action to verify user identity"""

    def name(self) -> Text:
        return "action_verify_identity"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # Get account number from entities or latest message
        account_number = None
        
        # Try to extract from entities
        entities = tracker.latest_message.get("entities", [])
        for entity in entities:
            if entity.get("entity") == "account_number":
                account_number = entity.get("value")
                break
        
        # If not found in entities, try to extract from text (simple pattern)
        if not account_number:
            text = tracker.latest_message.get("text", "")
            # Simple extraction - look for numbers
            words = text.split()
            for word in words:
                if word.isdigit() and len(word) >= 6:
                    account_number = word
                    break
        
        # Mock verification (in real system, this would check against database)
        # Accept any account number that's 6+ digits as valid for demo
        if account_number and len(str(account_number)) >= 6:
            # Set identity as verified
            requested_action = tracker.get_slot("requested_action")
            
            # If there was a pending action (balance or transactions), complete it automatically
            if requested_action == "check_balance":
                account_type = tracker.get_slot("account_type") or "checking"
                mock_balances = {
                    "checking": "$5,432.10",
                    "savings": "$12,345.67",
                    "default": "$5,432.10"
                }
                balance = mock_balances.get(account_type.lower(), mock_balances["default"])
                dispatcher.utter_message(
                    text=f"Identity verified. Your {account_type} account balance is {balance}. Is there anything else I can help with?"
                )
                return [
                    SlotSet("identity_verified", True), 
                    SlotSet("verification_attempts", 0.0),
                    SlotSet("requested_action", None)
                ]
            elif requested_action == "view_transactions":
                from datetime import datetime, timedelta
                today = datetime.now()
                mock_transactions = [
                    {"date": (today - timedelta(days=1)).strftime("%Y-%m-%d"), 
                     "description": "DEBIT CARD PURCHASE - COFFEE SHOP", 
                     "amount": "-$4.50"},
                    {"date": (today - timedelta(days=1)).strftime("%Y-%m-%d"), 
                     "description": "DIRECT DEPOSIT - SALARY", 
                     "amount": "+$3,500.00"},
                    {"date": (today - timedelta(days=2)).strftime("%Y-%m-%d"), 
                     "description": "ONLINE BILL PAY - UTILITIES", 
                     "amount": "-$125.00"},
                    {"date": (today - timedelta(days=3)).strftime("%Y-%m-%d"), 
                     "description": "ATM WITHDRAWAL", 
                     "amount": "-$100.00"},
                    {"date": (today - timedelta(days=4)).strftime("%Y-%m-%d"), 
                     "description": "TRANSFER FROM SAVINGS", 
                     "amount": "+$500.00"},
                ]
                transactions_text = "\n".join([
                    f"{tx['date']}: {tx['description']} {tx['amount']}"
                    for tx in mock_transactions
                ])
                dispatcher.utter_message(
                    text=f"Identity verified. Here are your recent transactions:\n\n{transactions_text}\n\nIs there anything else you need?"
                )
                return [
                    SlotSet("identity_verified", True), 
                    SlotSet("verification_attempts", 0.0),
                    SlotSet("requested_action", None)
                ]
            else:
                dispatcher.utter_message(
                    text="Identity verified successfully. How can I assist you?"
                )
                return [SlotSet("identity_verified", True), SlotSet("verification_attempts", 0.0)]
        else:
            verification_attempts = tracker.get_slot("verification_attempts") or 0.0
            verification_attempts += 1.0
            
            if verification_attempts >= 3.0:
                dispatcher.utter_message(
                    text="I'm sorry, I couldn't verify your identity after multiple attempts. "
                    "For your security, I can only provide general information. "
                    "Would you like to speak with a human agent?"
                )
                return [
                    SlotSet("identity_verified", False),
                    SlotSet("verification_attempts", 0.0)
                ]
            else:
                dispatcher.utter_message(
                    text="I need a valid account number (6+ digits) to verify your identity. "
                    "Please provide your account number."
                )
                return [SlotSet("verification_attempts", verification_attempts)]
        
        return []


class ActionSetIdentityVerified(Action):
    """Action to set identity verified flag"""

    def name(self) -> Text:
        return "action_set_identity_verified"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        return [SlotSet("identity_verified", True)]


class ActionLostCardFlow(Action):
    """Action to handle lost/stolen card flow"""

    def name(self) -> Text:
        return "action_lost_card_flow"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # Check if there's a pending verification request and user provided a number
        # If so, handle verification instead of lost card
        requested_action = tracker.get_slot("requested_action")
        text = tracker.latest_message.get("text", "").strip()
        
        # Check if the message contains only numbers (likely account number)
        if requested_action and text.isdigit() and len(text) >= 6:
            # User is providing account number for verification, not reporting lost card
            # Call verification action directly
            account_number = text
            # Set identity as verified and complete the requested action
            if requested_action == "check_balance":
                account_type = tracker.get_slot("account_type") or "checking"
                mock_balances = {
                    "checking": "$5,432.10",
                    "savings": "$12,345.67",
                    "default": "$5,432.10"
                }
                balance = mock_balances.get(account_type.lower(), mock_balances["default"])
                dispatcher.utter_message(
                    text=f"Identity verified. Your {account_type} account balance is {balance}. Is there anything else I can help with?"
                )
                return [
                    SlotSet("identity_verified", True), 
                    SlotSet("verification_attempts", 0.0),
                    SlotSet("requested_action", None)
                ]
            elif requested_action == "view_transactions":
                from datetime import datetime, timedelta
                today = datetime.now()
                mock_transactions = [
                    {"date": (today - timedelta(days=1)).strftime("%Y-%m-%d"), 
                     "description": "DEBIT CARD PURCHASE - COFFEE SHOP", 
                     "amount": "-$4.50"},
                    {"date": (today - timedelta(days=1)).strftime("%Y-%m-%d"), 
                     "description": "DIRECT DEPOSIT - SALARY", 
                     "amount": "+$3,500.00"},
                    {"date": (today - timedelta(days=2)).strftime("%Y-%m-%d"), 
                     "description": "ONLINE BILL PAY - UTILITIES", 
                     "amount": "-$125.00"},
                    {"date": (today - timedelta(days=3)).strftime("%Y-%m-%d"), 
                     "description": "ATM WITHDRAWAL", 
                     "amount": "-$100.00"},
                    {"date": (today - timedelta(days=4)).strftime("%Y-%m-%d"), 
                     "description": "TRANSFER FROM SAVINGS", 
                     "amount": "+$500.00"},
                ]
                transactions_text = "\n".join([
                    f"{tx['date']}: {tx['description']} {tx['amount']}"
                    for tx in mock_transactions
                ])
                dispatcher.utter_message(
                    text=f"Identity verified. Here are your recent transactions:\n\n{transactions_text}\n\nIs there anything else you need?"
                )
                return [
                    SlotSet("identity_verified", True), 
                    SlotSet("verification_attempts", 0.0),
                    SlotSet("requested_action", None)
                ]
        
        # Get card type from entities or slot
        card_type = tracker.get_slot("card_type")
        if not card_type:
            # Try to get from entities
            entities = tracker.latest_message.get("entities", [])
            for entity in entities:
                if entity.get("entity") == "card_type":
                    card_type = entity.get("value")
                    break
        
        if not card_type or card_type == "None":
            card_type = "card"
        
        dispatcher.utter_message(
            text=f"I'm sorry to hear that your {card_type} has been lost or stolen. "
            "This must be stressful. I can help guide you through the steps to protect your account."
        )
        
        dispatcher.utter_message(
            text=(
                "Here are the steps to secure your account:\n"
                "1. Freeze your card immediately to prevent unauthorized use\n"
                "2. Report the incident through our online portal or mobile app\n"
                "3. Request a replacement card\n"
                "4. Monitor your account for any suspicious activity\n\n"
                "For security reasons, I cannot freeze your card directly through this chat. "
                "Would you like me to connect you with a human agent who can process these actions immediately?"
            )
        )
        
        return []


class ActionGeneralFAQ(Action):
    """Action to handle general FAQ queries"""

    def name(self) -> Text:
        return "action_general_faq"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # Simple FAQ matching (in production, this could use a knowledge base or LLM)
        text = tracker.latest_message.get("text", "").lower()
        
        faq_responses = {
            "hours": "Our branch hours are Monday-Friday: 9:00 AM - 5:00 PM, "
                     "Saturday: 9:00 AM - 2:00 PM. Online and mobile banking are available 24/7.",
            "open": "Our branches are open Monday-Friday: 9:00 AM - 5:00 PM, "
                    "Saturday: 9:00 AM - 2:00 PM.",
            "services": "We offer checking accounts, savings accounts, credit cards, "
                       "loans, mortgages, investment services, and online/mobile banking.",
            "minimum balance": "Our checking account requires a minimum balance of $100. "
                             "Savings accounts have no minimum balance requirement.",
            "interest rates": "Current interest rates vary by account type. "
                            "Please visit our website or contact a branch for current rates.",
            "fees": "Our fee schedule depends on the account type. "
                   "Most basic accounts have no monthly fees. "
                   "Please check our website or speak with an agent for details.",
            "transfer money": "You can transfer money using online banking, mobile app, "
                            "or by visiting a branch. Online and mobile transfers are instant.",
            "pay bills": "You can pay bills through online banking or our mobile app. "
                        "Simply add a payee and schedule payments.",
            "password": "To change your password, log in to online banking, "
                       "go to Settings > Security > Change Password. "
                       "For password reset, click 'Forgot Password' on the login page.",
            "address": "To update your address, log in to online banking and go to "
                      "Profile > Personal Information, or visit a branch with valid ID.",
            "mobile banking": "Our mobile banking app is available for iOS and Android. "
                            "Download it from the App Store or Google Play Store.",
            "online banking": "Online banking is available 24/7. "
                            "Register at our website using your account number and personal information.",
        }
        
        # Match keywords
        answer = None
        for keyword, response in faq_responses.items():
            if keyword in text:
                answer = response
                break
        
        if not answer:
            # Default response
            answer = (
                "I can help you with information about our banking services, "
                "account features, branch locations, and general inquiries. "
                "For specific account information, I'll need to verify your identity first. "
                "Is there something specific you'd like to know?"
            )
        
        dispatcher.utter_message(text=answer)
        
        return []


class ActionFallbackHandler(Action):
    """Action to handle unknown queries - can integrate GPT-based component here"""

    def name(self) -> Text:
        return "action_fallback_handler"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        # This is where you could integrate a GPT-based component
        # For now, we'll provide a helpful fallback
        
        dispatcher.utter_message(
            text=(
                "I'm not entirely sure how to help with that. "
                "I can assist with:\n"
                "- Checking account balance\n"
                "- Viewing recent transactions\n"
                "- Finding branch locations\n"
                "- Lost or stolen card assistance\n"
                "- General banking questions\n\n"
                "If you need help with something else, I can connect you with a human agent. "
                "Would you like to speak with someone?"
            )
        )
        
        return []


# GPT-based fallback handler (commented out - to be used with proper guardrails)
"""
class ActionGPTFallbackHandler(Action):
    \"\"\"Action to handle unknown queries using GPT (with guardrails)\"\"\"

    def name(self) -> Text:
        return "action_fallback_handler"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> List[Dict[Text, Any]]:
        import openai
        
        user_message = tracker.latest_message.get("text", "")
        
        # Guardrails: System prompt with restrictions
        system_prompt = (
            "You are a helpful bank customer service assistant. "
            "IMPORTANT RULES:\n"
            "1. NEVER provide actual account numbers, balances, or sensitive information\n"
            "2. NEVER perform financial transactions\n"
            "3. If asked about account-specific information, always require identity verification\n"
            "4. If unsure, always offer to connect to a human agent\n"
            "5. Keep responses concise and helpful\n"
            "6. Only discuss general banking topics\n"
        )
        
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
            
            # Additional guardrail: Check for sensitive keywords
            sensitive_keywords = ["account number", "ssn", "social security", "pin"]
            if any(keyword in answer.lower() for keyword in sensitive_keywords):
                answer = "I'm sorry, I cannot provide sensitive information. Please speak with a human agent."
            
            dispatcher.utter_message(text=answer)
            
        except Exception as e:
            dispatcher.utter_message(
                text="I'm having trouble understanding that. Would you like to speak with a human agent?"
            )
        
        return []
"""

