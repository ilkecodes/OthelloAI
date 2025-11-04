"""Test Instagram location data"""
import os
from apify_client import ApifyClient

client = ApifyClient(os.getenv("APIFY_API_TOKEN"))

# Test search
print("🧪 Testing Instagram search with location...")

run = client.actor("apify/instagram-profile-scraper").call(
    run_input={
        "usernames": ["istanbulfoodblogger", "ankarafitness"],  # Test usernames
        "resultsLimit": 5
    },
    timeout_secs=60
)

print("\n📊 Data fields returned:")
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(f"\nUsername: {item.get('username')}")
    print(f"Biography: {item.get('biography', 'N/A')}")
    print(f"Location: {item.get('location', 'N/A')}")
    print(f"City: {item.get('city', 'N/A')}")
    print(f"Country: {item.get('country', 'N/A')}")
    print(f"All keys: {list(item.keys())}")
    break
