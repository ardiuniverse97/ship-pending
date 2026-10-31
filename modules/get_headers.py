import requests

# GET HEADERS
def get_headers(auth_headers_url):
  resonse=requests.get(auth_headers_url).json()
  return {
    "accept": "*/*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "authorization": resonse['authorization'],
    "cookie": resonse['cookie'],
    "priority": "u=1, i",
    "referer": "https://seller.shopee.co.id/webchat/conversations",
    "sec-ch-ua": "'Chromium';v='140', 'Not=A?Brand';v='24', 'Google Chrome';v='140'",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "'Windows'",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36",
    "x-shop-region": "ID"
  }