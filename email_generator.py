import requests
import random
import pyperclip
import time
import os
from pprint import pprint
from typing import Set

# Useful information
# https://www.1secmail.com/api/#
# ENDPOINTS
# BASEURL = "https://www.1secmail.com/api/v1/"
# ACTIVE_DOMAIN_LIST_ENDPOINT = "https://www.1secmail.com/api/v1/?action=getDomainList"
GENERATE_RANDOM_EMAIL_ENDPOINT = "https://www.1secmail.com/api/v1/?action=genRandomMailbox"


def generate_email() -> str:
    """Return a randomly generated email from the 1secmail endpoint"""
    r = requests.get(GENERATE_RANDOM_EMAIL_ENDPOINT)
    email = r.json()[0]
    return email


def parse_email(email: str) -> Set[str]:
    """Splits the email into two parts: the username and the mail server/domain and returns as a set"""
    user = email.split('@')[0]
    domain = email.split('@')[1]
    return (user, domain)


def list_of_emails(email) -> list:
    """Returns a list of the emails in the mailbox on 1secmail given an email"""
    user, domain = parse_email(email)

    list_of_emails_endpoint = f"https://www.1secmail.com/api/v1/?action=getMessages&login={
        user}&domain={domain}"

    r = requests.get(list_of_emails_endpoint)

    return r.json()


def clear_screen() -> None:
    """Clears the terminal screen"""
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = system('clear')


def print_emails(emails: list, email: str) -> None:
    """Takes a list of emails and prints each email to the screen"""
    user, domain = parse_email(email)
    for mail in emails:
        id = mail['id']

        r = requests.get(
            f'https://www.1secmail.com/api/v1/?action=readMessage&login={user}&domain={domain}&id={id}')
        content = r.json()
        print(f"\nDate: {content['date']}\nFrom: {content['from']}\n\tSubject: {
              content['subject']}\n\tBody: {content['textBody']}")


def main():
    count = 0

    # Generate the email
    email = generate_email()

    # Copy the email to clipboard
    pyperclip.copy(email)
    print(f"Your email has been copied to clipboard - {email}\n")

    while True:
        if len(list_of_emails(email)) > count:
            count += 1
            clear_screen()
            # This contains an email
            print_emails(list_of_emails(email), email)
            command = input("Read more emails: (y/n): ")
            match command:
                case 'y':
                    continue
                case 'n':
                    break
        else:
            # This does not contain email
            print("Checking for email")
            time.sleep(5)
            continue


if __name__ == "__main__":
    main()
