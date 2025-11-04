from pytrends.request import TrendReq
import sys

print("Testing Google Trends...")

try:
    pytrends = TrendReq(hl='tr-TR', tz=180)
    
    keywords = ["viral", "trend", "popüler"]
    
    print(f"Building payload for: {keywords}")
    pytrends.build_payload(keywords, cat=0, timeframe='now 7-d', geo='TR')
    
    print("Getting interest over time...")
    data = pytrends.interest_over_time()
    
    print(f"\nData shape: {data.shape}")
    print(f"Columns: {data.columns.tolist()}")
    print(f"\nFirst few rows:")
    print(data.head())
    
    print("\n✅ Google Trends is working!")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
