import requests

# API URL
url = "https://api.investing.com/api/financialdata/41063/historical/chart/"

# Query Parameters
params = {
    "interval": "P1D",
    "period": "MAX",
    "pointscount": 160
}

# Send GET request
response = requests.get(url, params=params)

# Check response
if response.status_code == 200:
    data = response.json()  # Convert response to JSON
    print(data)  # Print or process the data
else:
    print(f"Error {response.status_code}: {response.text}")

