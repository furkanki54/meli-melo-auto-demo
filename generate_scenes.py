import requests

url = "https://web-production-c6b3.up.railway.app/bulk-generate"

response = requests.post(url, json={})
print("Durum:", response.status_code)
print("Yanıt:", response.json())
