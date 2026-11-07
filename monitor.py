import urllib.request
import urllib.parse
import json
import os
import time

def get_cloudflare_data(token):
    print("--- Checking Cloudflare ---")
    if not token:
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
    until = int(time.time())
    from_time = until - (24 * 60 * 60) # 24 ساعت گذشته
    
    base_url = "https://api.ioda.inetintel.cc.gatech.edu/v2/signals/raw/country/IR"
    params = {"from": from_time, "until": until, "source": source}
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            if data.get('data') and len(data['data']) > 0:
                for item in data['data'][0]:
                    if isinstance(item, dict) and item.get('datasource') == source:
                        values = [v for v in item.get('values', []) if v is not None]
                        if values:
                            current_val = values[-1] # آخرین مقدار
                            avg_val = sum(values) / len(values) # میانگین ۲۴ ساعت
                            
                            # محاسبه درصد افت
                            drop_percent = 0
                            if avg_val > 0:
                                drop_percent = ((avg_val - current_val) / avg_val) * 100
                            
                            # اگر افت بیش از ۲۰ درصد بود، هشدار بده
                            status = "Warning" if drop_percent > 20 else "Normal"
                            
                            return {
                                "current": current_val,
                                "average": int(avg_val),
                                "drop_percent": round(drop_percent, 1),
                                "status": status
                            }
            return None
    except Exception as e:
        print(f"IODA Error ({source}): {e}")
        return None

def main():
    print("Starting Iran Internet Monitor (CF + IODA)...")
    cf_token = os.environ.get("CF_API_TOKEN")
    
    cf_data = get_cloudflare_data(cf_token)
    bgp_data = get_ioda_signal("bgp")
    ping_data = get_ioda_signal("ping-slash24")

    output = {
        "status": "Success" if cf_data else "Partial",
        "last_run": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "cloudflare": cf_data if cf_data else {"error": "Failed"},
        "ioda": {
            "bgp": bgp_data if bgp_data else {"current": "N/A", "status": "Unknown"},
            "ping": ping_data if ping_data else {"current": "N/A", "status": "Unknown"}
        }
    }

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(output, f, indent=4)
    print("Data saved to data.json")
    print(f"Final Output: {json.dumps(output['ioda'], indent=2)}")

if __name__ == "__main__":
    main()
