import urllib.request
import urllib.parse
import json
import os
from datetime import datetime

def check_cloudflare_traffic():
    print("Starting Iran Internet Monitor...")
    token = os.environ.get("CF_API_TOKEN")
    
    if not token:
        print("Warning: Cloudflare API Token not found.")
        return

    base_url = "https://api.cloudflare.com/client/v4/radar/netflows/summary"
    params = {
        "location": "IR",
        "dateRange": "7d",
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
            
            # استخراج داده‌های مهم
            result = data.get('result', {})
            summary = result.get('summary_0', {})
            meta = result.get('meta', {})
            
            http_percent = summary.get('HTTP', '0')
            other_percent = summary.get('OTHER', '0')
            last_updated = meta.get('lastUpdated', 'Unknown')
            confidence = meta.get('confidenceInfo', {}).get('level', 'Unknown')

            # ساخت دیکشنری خروجی
            output_data = {
                "last_updated": last_updated,
                "http_traffic_percentage": http_percent,
                "other_traffic_percentage": other_percent,
                "confidence_level": confidence,
                "status": "Success"
            }

            # ذخیره در فایل data.json
            with open('data.json', 'w', encoding='utf-8') as f:
                json.dump(output_data, f, indent=4)
            
            print("Data saved to data.json successfully.")
            print(json.dumps(output_data, indent=2))

    except urllib.error.HTTPError as e:
        error_body = e.read().decode()
        print(f"HTTP Error {e.code}: {e.reason}")
        print(f"Error details: {error_body}")
    except Exception as e:
        print(f"Error connecting to Cloudflare: {e}")

if __name__ == "__main__":
    check_cloudflare_traffic()
