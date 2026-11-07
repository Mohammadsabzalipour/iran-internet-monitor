import urllib.request
import urllib.parse
import json
import os
import time

def get_cloudflare_data(token):
    print("--- Checking Cloudflare ---")
    if not token:
        print("Warning: CF_API_TOKEN not found.")
        return None
    base_url = "https://api.cloudflare.com/client/v4/radar/netflows/summary"
    params = {"location": "IR", "dateRange": "7d", "format": "json"}
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    headers = {"Authorization": f"Bearer {token}"}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            summary = data.get('result', {}).get('summary_0', {})
            return {
                "http_percent": summary.get('HTTP', '0'),
                "other_percent": summary.get('OTHER', '0'),
                "last_updated": data.get('result', {}).get('meta', {}).get('lastUpdated')
            }
    except Exception as e:
        print(f"Cloudflare Error: {e}")
        return None

def get_ioda_signal(source):
    print(f"--- Checking IODA: {source} ---")
    # بازه ۲۴ ساعت گذشته
    until = int(time.time())
    from_time = until - (24 * 60 * 60)
    
    base_url = "https://api.ioda.inetintel.cc.gatech.edu/v2/signals/raw/country/IR"
    params = {
        "from": from_time,
        "until": until,
        "source": source
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    print(f"Requesting: {url}")
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            # ساختار داده IODA شامل لیستی از نقاط داده است
            if data.get('data') and len(data['data']) > 0:
                # آخرین نقطه داده موجود را برمی‌گردانیم
                latest_point = data['data'][-1]
                return latest_point.get('value')
            return None
    except Exception as e:
        print(f"IODA Error ({source}): {e}")
        return None

def main():
    print("Starting Iran Internet Monitor (CF + IODA)...")
    cf_token = os.environ.get("CF_API_TOKEN")
    
    # دریافت داده‌ها
    cf_data = get_cloudflare_data(cf_token)
    bgp_val = get_ioda_signal("bgp")
    ping_val = get_ioda_signal("ping-slash24")

    # ساخت خروجی نهایی
    output = {
        "status": "Success" if cf_data else "Partial",
        "last_run": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cloudflare": cf_data if cf_data else {"error": "Failed"},
        "ioda": {
            "bgp_value": bgp_val,
            "active_probing_value": ping_val
        }
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4)
    print("Data saved to data.json")

if __name__ == "__main__":
    main()
