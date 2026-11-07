import urllib.request
import json
import os

def check_cloudflare_traffic():
    print("Starting Iran Internet Monitor...")
    # دریافت توکن از تنظیمات گیت‌هاب
    token = os.environ.get("CF_API_TOKEN") 
    
    if not token:
        print("Warning: Cloudflare API Token not found. Please add it in Settings > Secrets.")
        return

    # آدرس API کلادفلر برای دریافت ترافیک ایران (کد دو حرفی ایران IR است)
    url = "https://api.cloudflare.com/client/v4/radar/traffic/summary?location=IR"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            print("Successfully connected to Cloudflare Radar.")
            # در اینجا می‌توانید داده‌های دریافتی را پرینت کنید
            print(f"Data received: {data}")
    except Exception as e:
        print(f"Error connecting to Cloudflare: {e}")

if __name__ == "__main__":
    check_cloudflare_traffic()
