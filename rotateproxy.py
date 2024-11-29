import requests
from itertools import cycle

# Simulated list of proxy IPs (replace with real proxies)
proxy_ips = [
    '147.93.128.199:8888',
    '200.174.198.86:8888',
    '3.71.23.219:8090',
]

# Maximum number of requests per proxy
MAX_REQUESTS_PER_PROXY = 10

# Simulate making a request to a mobile app's server
def make_request(proxy):
    url = 'https://jsonplaceholder.typicode.com/posts'  # The mobile app's server URL
    try:
        response = requests.get(url, proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"})
        return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"Error with proxy {proxy}: {e}")
        return None

# Function to rotate proxies and limit requests per proxy
def rotate_proxies(proxies, max_requests):
    proxy_cycle = cycle(proxies)  # Infinite iterator over proxy list
    proxy_request_count = {proxy: 0 for proxy in proxies}  # Track request counts per proxy

    request_count = 0
    while request_count < 100:  # Arbitrary number of total requests to make
        proxy = next(proxy_cycle)  # Get the next proxy from the cycle
        if proxy_request_count[proxy] < max_requests:
            status_code = make_request(proxy)
            if status_code:
                print(f"Request to {proxy} was successful. Status Code: {status_code}")
                proxy_request_count[proxy] += 1
                request_count += 1
            else:
                print(f"Request to {proxy} failed.")
        else:
            print(f"Proxy {proxy} has reached the maximum request limit.")
            continue

# Main function to start the request rotation
def main():
    print("Starting request rotation...")
    rotate_proxies(proxy_ips, MAX_REQUESTS_PER_PROXY)

if __name__ == "__main__":
    main()
