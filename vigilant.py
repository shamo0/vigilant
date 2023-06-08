import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from urllib.parse import urlparse
import argparse
from collections import deque
import time
import sys

# Webhooks for alerts
# discord_webhook = "https://discord.com/api/webhooks/<your-discord-webhook>"

def monitor_forums(company_domain, base_url, depth_limit=None):
    #Crawl the website
    print("##########################################################")
    print("Searching mentions of %s in %s" % (company_domain,base_url))
    print("##########################################################")
    visited_urls = set()  # Track visited URLs to avoid infinite loops
    urls_to_visit = deque([(base_url, 0)])  # Initialize the deque of URLs to visit with depth

    while urls_to_visit:
        url, depth = urls_to_visit.popleft()

        if url in visited_urls:
            continue

        visited_urls.add(url)

        try:
            response = requests.get(url)
            if response.status_code == 200:
                # Check if company domain appears in the webpage content
                if company_domain.lower() in response.text.lower():
                    print(f"Alert: Company domain '{company_domain}' found at URL: {url}")

                    # Uncomment the below 2 lines to use Discord alerting
                    # message = f"Alert: Company domain '{company_domain}' found at URL: {url}"
                    # send_notification(message, discord_webhook)
                
                if depth_limit is None or depth < depth_limit:
                    # Extract links from the webpage and add them to the deque of URLs to visit with updated depth
                    soup = BeautifulSoup(response.content, "html.parser")
                    for link in soup.find_all("a"):
                        href = link.get("href")
                        absolute_url = urljoin(base_url, href)
                        parsed_url = urlparse(absolute_url)
                        if parsed_url.netloc == urlparse(base_url).netloc and absolute_url not in visited_urls:
                            urls_to_visit.append((absolute_url, depth + 1))

        except requests.exceptions.RequestException as e:
            print(f"Error accessing URL: {url} - {str(e)}")   

def forum_search(domain):
    forum_file = "forums.txt"
    # Open the file and read its contents
    with open(forum_file, "r") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    # Call the monitor_forums() function with the provided domain
    for forum_path in lines:
        monitor_forums(domain,forum_path)

def darknet_forum_search(domain):
    #configure SOCKS proxy (update based on your configuration specification)
    try:
        socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
        socket.socket = socks.socksocket
    except:
        print("Make Sure to start the TOR service")
        quit()
    # open onion_forums.txt and read its contents
    onion_file = "onion_forums.txt"
    with open(onion_file, "r") as file:
        lines = file.readlines()
    lines = [line.strip() for line in lines]
    
    #for each onion domain, do checks.
    for darknet_forum_path in lines:
        monitor_forums(domain, darknet_forum_path)
        change_tor_circuit() # Change tor circuit

def change_tor_circuit():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate()  # Provide the necessary authentication
        controller.signal(Signal.NEWNYM)

def send_notification(message, webhook_url):
    payload = {'content': message}

    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("Notification sent successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending notification: {str(e)}")

def main():
    print(r"""
    __     __ _         _  _                _
    \ \   / /(_)  __ _ (_)| |  __ _  _ __  | |_
     \ \ / / | | / _` || || | / _` || '_ \ | __|
      \ V /  | || (_| || || || (_| || | | || |_
       \_/   |_| \__, ||_||_| \__,_||_| |_| \__|
                |___/
                                     by shamo0
    """)
    # parse command line args
    parser = argparse.ArgumentParser(description='Vigilant -- Monitor your breaches!')
    parser.add_argument('-d', '--domain', help='Domain to monitor in the forums')
    parser.add_argument('--surface', action='store_true', help='(Default) Enable surface web search.')
    parser.add_argument('--dark', action='store_true', help='Enable Onion search. TOR service needs to be started')
    parser.add_argument('--dark-only', action='store_true', help='Enable Onion ONLY search. TOR service needs to be started')
    parser.add_argument('-l', '--limit', help='Set depth limit (Default=3)')
    parser.add_argument('-k', '--keep-alive', action='store_true', help='Keep the program running after execution')
    # Set the default value for the options
    parser.set_defaults(surface=True, limit=3)
    args = parser.parse_args()

    # Check if help is requested
    if args.domain is None:
        parser.print_help()
        return
    try:
        while True:
            if args.surface:
                forum_search(args.domain)
                if not args.keep_alive:
                    quit()
            
            if args.dark_only:
                import socks
                import socket
                import stem
                darknet_forum_search(args.domain)
                if not args.keep_alive:
                    quit()

            if args.dark:
                import socks
                import socket
                import stem
                forum_search(args.domain)
                darknet_forum_search(args.domain)
                if not args.keep_alive:
                    quit()
            
            print("Restarting the program in 60 seconds...")
            time.sleep(60)  # Wait for 60 seconds before restarting
    except KeyboardInterrupt:
        print("\nBye!")
        sys.exit(0)
if __name__ == '__main__':
    main()