from colorama import Fore, Style
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, parse_qs
import subprocess
import whois
import wafw00f

def x0rec():
    header = r'''
  _______  _______  _______  _______
 (  ____ \(  ___  )(  ____ \(  ___  )
 | (    \/| (   ) || (    \/| (   ) |
 | (_____ | |   | || |      | (___) |
 (_____  )| |   | || | ____ |  ___  |
       ) || |   | || | \_  )| (   ) |gg
 /\____) || (___) || (___) || )   ( |
 \_______)(_______)(_______)|/     \|
    '''
    print(Fore.BLUE + Style.BRIGHT + header)

x0rec()

def domainInput():
    global domain, domainProtocol
    domain = input(Fore.BLUE + Style.DIM + "Enter the domain without protocol: ")
    domainProtocol = int(input("Is it HTTP or HTTPS [1/2]: "))
    if domainProtocol == 1:
        domain = "http://" + domain
    else:
        domain = "https://" + domain

    def validateDomain(domain):
        try:
            global response
            response = requests.get(domain)
            if response.ok:
                return True
        except:
            print(Fore.RED + Style.DIM + "Invalid Domain\nRetry:")
            domainInput()
            pass

    if validateDomain(domain):
        return True

domainInput()
print(Fore.GREEN + Style.DIM + domain + Fore.WHITE + Style.DIM)

unique_urls = set()

def extract_parameters(url, page_url):
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    if query_params:
        print(Fore.YELLOW + Style.BRIGHT + "URL:", page_url)
        for key, value in query_params.items():
            print(Fore.CYAN + Style.BRIGHT + f"Parameter: {key}, Value(s): {', '.join(value)}")

def crawl_website(url):
    if url not in unique_urls:
        unique_urls.add(url)
        try:
            soup = BeautifulSoup(response.content, 'html.parser')
            print(soup.get_text())

            links = soup.find_all('a')
            for link in links:
                href = link.get('href')
                if href:
                    extract_parameters(href, url)

        except requests.exceptions.RequestException as e:
            print(f"Request Exception: {e}")

        except Exception as e:
            print(f"An error occurred: {e}")

with ThreadPoolExecutor(max_workers=5) as executor:
    executor.map(crawl_website, [domain])

print(Fore.BLUE + Style.DIM)

def run_subfinder(url):
    try:
        subfinder_output = subprocess.check_output(['subfinder', '-d', url], universal_newlines=True)
        return subfinder_output
    except subprocess.CalledProcessError as e:
        return f"Error running Subfinder: {e}"

def run_assetfinder(url):
    try:
        assetfinder_output = subprocess.check_output(['assetfinder', url], universal_newlines=True)
        return assetfinder_output
    except subprocess.CalledProcessError as e:
        return f"Error running Assetfinder: {e}"

def run_wafw00f(url):
    try:
        wafw00f_output = wafw00f.wafw00f(url)
        return wafw00f_output
    except Exception as e:
        return f"Error running Wafw00f: {e}"

def run_whois(url):
    try:
        whois_info = whois.whois(url)
        return whois_info
    except Exception as e:
        return f"Error running Whois: {e}"

if __name__ == '__main__':
    url = domain

    print("Running Subfinder...")
    subfinder_result = run_subfinder(url)
    print("Subfinder Output:")
    print(subfinder_result)

    print("\nRunning Assetfinder...")
    assetfinder_result = run_assetfinder(url)
    print("Assetfinder Output:")
    print(assetfinder_result)

    print("\nRunning Wafw00f...")
    wafw00f_result = run_wafw00f(url)
    print("Wafw00f Output:")
    print(wafw00f_result)

    print("\nRunning Whois...")
    whois_info = run_whois(url)
    print("Whois Information:")
    print(whois_info)
