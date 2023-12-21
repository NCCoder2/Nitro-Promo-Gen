import requests
import threading
from datetime import datetime, timedelta
from colorama import Fore, Style
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

COLOR_ERROR = Fore.RED
COLOR_SUCCESS = Fore.GREEN
COLOR_INFO = Fore.CYAN

count = 0
print_lock = threading.Lock()
start_time_global = datetime.now()

def check_proxy(proxy):
    try:
        response = requests.get("https://example.com", proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"}, timeout=3)
        response.raise_for_status()  
        print(COLOR_SUCCESS + f"Valid Proxy: {proxy}" + Style.RESET_ALL)
        return True
    except Exception as e:
        print(COLOR_ERROR + f"Invalid Proxy: {proxy}" + Style.RESET_ALL)
    return False

def generate_promo(session, proxy):
    global count

    try:
        start_time = datetime.now()

        if proxy:
            response = requests.options(
                "https://api.discord.gx.games/v1/direct-fulfillment",
                headers={
                    "authority": "api.discord.gx.games",
                    "method": "OPTIONS",
                    "path": "/v1/direct-fulfillment",
                    "scheme": "https",
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9",
                    "access-control-request-headers": "content-type",
                    "access-control-request-method": "POST",
                    "origin": "https://www.opera.com",
                    "referer": "https://www.opera.com/",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "cross-site",
                },
                proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                verify=False,
            )
        else:
            response = requests.options(
                "https://api.discord.gx.games/v1/direct-fulfillment",
                headers={
                    "authority": "api.discord.gx.games",
                    "method": "OPTIONS",
                    "path": "/v1/direct-fulfillment",
                    "scheme": "https",
                    "accept": "*/*",
                    "accept-encoding": "gzip, deflate, br",
                    "accept-language": "en-US,en;q=0.9",
                    "access-control-request-headers": "content-type",
                    "access-control-request-method": "POST",
                    "origin": "https://www.opera.com",
                    "referer": "https://www.opera.com/",
                    "sec-fetch-dest": "empty",
                    "sec-fetch-mode": "cors",
                    "sec-fetch-site": "cross-site",
                },
                verify=False,
            )

        end_time = datetime.now()

        if response.status_code == 429:
            print_with_timestamp(COLOR_ERROR + "Rate Limited" + Style.RESET_ALL)
        else:
            count += 1
            token = response.headers.get("token")
            promo_link = f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}"

            with open("promos.txt", "a") as f:
                f.write(promo_link + "\n")

            duration = end_time - start_time
            print_with_timestamp(COLOR_SUCCESS + f"{count} Promo Generated in {duration}" + Style.RESET_ALL)

    except Exception as e:
        print_with_timestamp(COLOR_ERROR + f"Rate Limited" + Style.RESET_ALL)

def print_with_timestamp(message, header=False, subheader=False):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with print_lock:
        if header:
            print(f"{timestamp} {COLOR_INFO + message.upper() + Style.RESET_ALL}")
        elif subheader:
            print(f"{timestamp} {COLOR_INFO + message.capitalize() + Style.RESET_ALL}")
        else:
            print(f"{timestamp} {message}")

def main():
    global start_time_global
    print("\033[95m" + """
███╗░░██╗██╗████████╗██████╗░░█████╗░  ░██████╗░███████╗███╗░░██╗
████╗░██║██║╚══██╔══╝██╔══██╗██╔══██╗  ██╔════╝░██╔════╝████╗░██║
██╔██╗██║██║░░░██║░░░██████╔╝██║░░██║  ██║░░██╗░█████╗░░██╔██╗██║
██║╚████║██║░░░██║░░░██╔══██╗██║░░██║  ██║░░╚██╗██╔══╝░░██║╚████║
██║░╚███║██║░░░██║░░░██║░░██║╚█████╔╝  ╚██████╔╝███████╗██║░╚███║
╚═╝░░╚══╝╚═╝░░░╚═╝░░░╚═╝░░╚═╝░╚════╝░  ░╚═════╝░╚══════╝╚═╝░░╚══╝
""" + "\033[0m")


    use_proxies = input("Do you want to use proxies? (yes/no): ").lower() == 'yes'

    if use_proxies:
        proxies = []
        with open("proxies.txt", "r") as proxy_file:
            proxies = [line.strip() for line in proxy_file]

        valid_proxies = [proxy for proxy in proxies if check_proxy(proxy)]

        if not valid_proxies:
            print_with_timestamp(COLOR_ERROR + "No valid proxies found. Exiting." + Style.RESET_ALL)
            return

        print("\033[94m" + "Checking proxies done. Generating promos..." + "\033[0m")

    else:
        valid_proxies = [None]
        print_with_timestamp("Proceeding without proxies...", subheader=True)

    session = requests.Session()
    session.headers.update(
        {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 OPR/106.0.0.0"}
    )

    num_promos = int(input("Enter the number of promos to generate: "))
    num_threads = int(input("Enter the number of threads: "))

    threads = []
    for i in range(num_promos):
        thread = threading.Thread(target=generate_promo, args=(session, valid_proxies[0]))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    end_time_global = datetime.now()
    total_duration = end_time_global - start_time_global
    print_with_timestamp(f"Complete! Total time: {total_duration}", subheader=True)

if __name__ == "__main__":
    main()
