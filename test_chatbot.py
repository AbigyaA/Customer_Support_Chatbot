#!/usr/bin/env python3
"""
Simple test script to demonstrate chatbot functionality
This script can be used to test the chatbot after training
"""

import requests
import json

# Configuration
RASA_API_URL = "http://localhost:5005/webhooks/rest/webhook"

def send_message(message, sender_id="test_user"):
    """Send a message to the Rasa chatbot"""
    payload = {
        "sender": sender_id,
        "message": message
    }
    
    try:
        response = requests.post(RASA_API_URL, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Rasa server: {e}")
        print("Make sure the Rasa server is running on http://localhost:5005")
        return None

def test_conversation():
    """Test a sample conversation flow"""
    
    print("=" * 60)
    print("Bank Customer Service Chatbot - Test Conversation")
    print("=" * 60)
    print()
    
    # Test 1: Greeting
    print("Test 1: Greeting")
    print("-" * 60)
    responses = send_message("Hello")
    if responses:
        for response in responses:
            print(f"Bot: {response.get('text', '')}")
    print()
    
    # Test 2: Branch Locator
    print("Test 2: Branch Locator")
    print("-" * 60)
    responses = send_message("Where is the nearest branch?")
    if responses:
        for response in responses:
            print(f"Bot: {response.get('text', '')}")
    print()
    
    # Test 3: Lost Card
    print("Test 3: Lost Card Report")
    print("-" * 60)
    responses = send_message("I lost my credit card")
    if responses:
        for response in responses:
            print(f"Bot: {response.get('text', '')}")
    print()
    
    # Test 4: Balance Check (without verification)
    print("Test 4: Balance Check (without verification)")
    print("-" * 60)
    responses = send_message("What's my balance?")
    if responses:
        for response in responses:
            print(f"Bot: {response.get('text', '')}")
    print()
    
    # Test 5: Balance Check (with verification)
    print("Test 5: Balance Check (with verification)")
    print("-" * 60)
    responses = send_message("My account number is 123456789")
    if responses:
        for response in responses:
            print(f"Bot: {response.get('text', '')}")
    print()
    
    # Test 6: Human Handoff
    print("Test 6: Human Handoff Request")
    print("-" * 60)
    responses = send_message("This isn't helping, I need to talk to someone")
    if responses:
        for response in responses:
            print(f"Bot: {response.get('text', '')}")
    print()
    
    # Test 7: Goodbye
    print("Test 7: Goodbye")
    print("-" * 60)
    responses = send_message("Bye")
    if responses:
        for response in responses:
            print(f"Bot: {response.get('text', '')}")
    print()
    
    print("=" * 60)
    print("Test conversation complete!")
    print("=" * 60)

if __name__ == "__main__":
    print("\nNote: Make sure you have:")
    print("1. Trained the model: rasa train")
    print("2. Started the action server: rasa run actions")
    print("3. Started the Rasa server: rasa shell --enable-api")
    print("\nPress Enter to start testing...")
    input()
    
    test_conversation()

