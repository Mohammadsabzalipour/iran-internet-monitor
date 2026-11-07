import urllib.request
import urllib.parse
import json
import os

def check_cloudflare_traffic():
    print("Starting Iran Internet Monitor...")
    token = os.environ.get("CF_API_TOKEN")
    
    if not token:
        print("Warning: Cloudflare API Token not found.")
        return

    # استفاده از آدرس صحیح برای دریافت خلاصه ترافیک شبکه (NetFlows)
    base_url = "https://api.cloudflare.com/client/v4/radar/netflows/summary"
    params = {
        "location": "IR",
        "dateRange": "7d",  # دریافت داده‌های ۷ روز گذشته
        "format": "json"
    }
    
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    print(f"Requesting URL: {url}")

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print("Successfully connected to Cloudflare Radar.")
            print(f"Response success: {data.get('success')}")
            if data.get('result'):
                print(f"Sample result: {json.dumps(data['result'], indent=2)[:500]}...")
    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Error details: {error_body}")
    except Exception as e:
        print(f"Error connecting to Cloudflare: {e}")

if __name__ == "__main__":
    check_cloudflare_traffic()
