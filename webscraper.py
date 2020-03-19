import argparse
import re
import requests
import sys


def argparser(*args, **kwargs):
    """parse a URL passed in as a command line argument"""
    parser = argparse.ArgumentParser(
        description="Perform transformation on input text.")
    parser.add_argument('url',
                        help='url of website to search')
    return parser.parse_args()


def text_retriever(webpage):
    """retrieves the text of the webpage at the specified url"""
    print("Reading website, this may take a minute")
    r = requests.get(webpage)
    print("Done reading website")
    return r.text


def info_finder(web_text):
    """ look for email addresses, URLs, and phone numbers
    included in the web text"""
    email_finder(web_text)
    url_finder(web_text)
    phone_finder(web_text)


def email_finder(web_text):
    e_re = r"\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*"
    emails_found = re.findall(e_re, web_text)
    if emails_found:
        emails_found = sorted(set(emails_found))
        print("\nEmails found in provided link:")
        for email in emails_found:
            print(email)
    else:
        print("No emails found")
    return emails_found


def url_finder(web_text):
    u_re = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|'
    u_re += r'[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    urls_found = re.findall(u_re, web_text)
    if urls_found:
        urls_found = sorted(set(urls_found))
        print("\nURLs found in provided link:")
        for url in urls_found:
            print(url)
    else:
        print("No URLS found")
    return (urls_found)


def phone_finder(web_text):
    """returns phone numbers found in web_text"""
    p_re = r'1?\W*([2-9][0-8][0-9])\W*([2-9][0-9]{2})'
    p_re += r'\W*([0-9]{4})(\se?x?t?(\d*))?'
    phone_numbers_found = re.findall(p_re, web_text)
    if phone_numbers_found:
        phone_numbers_found = sorted(set(phone_numbers_found))
        print("\nPhone numbers found in provided link:")
        for phone in phone_numbers_found:
            print("({}){}-{}".format(phone[0], phone[1], phone[2]))
    else:
        print("No phone numbers found.")
    return phone_numbers_found


def main(*args):
    webpage = argparser().url
    web_text = text_retriever(webpage)
    return info_finder(web_text)


if __name__ == "__main__":
    main(sys.argv[1:])
