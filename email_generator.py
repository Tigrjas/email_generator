import requests
import random
import pyperclip
import time
import os
import sys
import webbrowser
import re
from pprint import pprint
from typing import Set
import logging

# Useful information
# https://www.1secmail.com/api/#
# ENDPOINTS
# BASEURL = "https://www.1secmail.com/api/v1/"
# ACTIVE_DOMAIN_LIST_ENDPOINT = "https://www.1secmail.com/api/v1/?action=getDomainList"
GENERATE_RANDOM_EMAIL_ENDPOINT = "https://www.1secmail.com/api/v1/?action=genRandomMailbox"

logging.basicConfig(level=logging.INFO)


def generate_email() -> str:
    """Return a randomly generated email from the 1secmail endpoint"""
    try:
        r = requests.get(GENERATE_RANDOM_EMAIL_ENDPOINT)
        email = r.json()[0]
        return email
    except Exception as e:
        logging.error("Failed to generate email: %s", e)
        return ""


def split_email(email: str) -> Set[str]:
    """Splits the email into two parts: the username and the mail server/domain and returns as a set"""
    user = email.split('@')[0]
    domain = email.split('@')[1]
    return (user, domain)


def list_of_emails(email) -> list:
    """Returns a list of the emails in the mailbox on 1secmail given an email"""
    try:
        user, domain = split_email(email)
        list_of_emails_endpoint = f"https://www.1secmail.com/api/v1/?action=getMessages&login={
            user}&domain={domain}"
        r = requests.get(list_of_emails_endpoint)
        return r.json()

    except Exception as e:
        logging.error("Failed to retrieve list of emails: %s", e)
        return []


def clear_screen() -> None:
    """Clears the terminal screen"""
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = system('clear')


def contains_code(text: str) -> bool:
    pattern = r"\d{4,}"
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False


def print_code(text: str) -> None:
    pattern = r"\d{4,}"
    match = re.search(pattern, text)
    pyperclip.copy(match.group())
    print(f"Code found: {match.group()}\n(copied to clipboard)")


def print_email(email: str, email_list: list) -> None:
    """Take a list of emails and print to the screen argument index"""
    try:
        user, domain = split_email(email)
        id = email_list[0]['id']

        r = requests.get(
            f'https://www.1secmail.com/api/v1/?action=readMessage&login={user}&domain={domain}&id={id}')
        content = r.json()
        print(f"\nDate: {content['date']}\nFrom: {content['from']}\n\tSubject: {
            content['subject']}\n\tBody: {content['textBody']}")

        if contains_code(content['textBody']):
            print_code(content['textBody'])
    except Exception as e:
        logging.error("Failed to print email: %s", e)


def open_1secmail(email: str) -> None:
    user, domain = split_email(email)
    url = f"https://www.1secmail.com/?login={user}&domain={domain}"
    webbrowser.open_new(url)


def monitor_email(email: str) -> None:
    """This keeps the terminal open and monitors if there are emails coming in"""
    print("""
___________________________________

       Monitoring for Emails
___________________________________
    """)

    count = 0

    try:
        while True:
            email_list = list_of_emails(email)
            if len(email_list) > count:
                print_email(email, email_list)
                count = len(email_list)
            time.sleep(5)  # Sleep to prevent accessive API calls
    except KeyboardInterrupt:
        print(f"Program terminated")


def print_title() -> None:
    """A title before the program runs. Just for fun"""
    print("""
╔══════════════════════════════════╗
║ A _ A                            ║
║(='o'=)     Email Generator       ║
║(;;)(;;)                          ║
╚══════════════════════════════════╝
""")


def main():
    print_title()

    # Generate the email
    email = generate_email()

    if email:
        # Copy the email to clipboard
        pyperclip.copy(email)
        print(f"{email} - copied to clipboard\n")

        monitor_email(email)
    else:
        print("Failed to generate email. Exiting")


if __name__ == "__main__":
    main()
