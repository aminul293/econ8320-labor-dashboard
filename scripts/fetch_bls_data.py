import requests
import pandas as pd
import os

# Replace with your BLS API key
API_KEY = "72bd5ec7070048a99f4892a5b9221399"  # Replace with your actual API key

# BLS API URL
BASE_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"

# Define the series IDs to fetch (non-farm employment & unemployment rate)
series_ids = ["CES0000000001", "LNS14000000"]

# Define the time range
start_year = "2022"
end_year = "2023"

# Prepare the request payload
payload = {
    "seriesid": series_ids,
    "startyear": start_year,
    "endyear": end_year,
    "registrationkey": API_KEY,
}

# Send the POST request to BLS API
response = requests.post(BASE_URL, json=payload)

# Check the response status
if response.status_code == 200:
    data = response.json()  # Parse the JSON response
    results = []

    # Extract the data for each series
    for series in data["Results"]["series"]:
        series_id = series["seriesID"]
        for record in series["data"]:
            results.append({
                "series_id": series_id,
                "date": f"{record['year']}-{record['period'][1:]}",  # Format as YYYY-MM
                "value": float(record["value"])
            })

    # Convert results into a DataFrame
    df = pd.DataFrame(results)

    # Ensure the "data" directory exists
    os.makedirs("data", exist_ok=True)

    # Debugging statement to confirm file saving
    print("Saving file to: data/bls_data.csv")

    # Save to CSV

