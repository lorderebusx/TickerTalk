import json
import os

# Use forward slashes for Windows compatibility in Python
mappingOutputPath = "E:/TickerTalk/data/masterMapping.json"

def generateMasterMapping():
    # Ensure the target directory exists
    os.makedirs(os.path.dirname(mappingOutputPath), exist_ok=True)
    
    masterMap = {
        "AAPL": {"cik": "0000320193", "file": "CIK0000320193.json", "companyName": "Apple Inc."},
        "WMT": {"cik": "0000104169", "file": "CIK0000104169.json", "companyName": "Walmart Inc."},
        "MSFT": {"cik": "0000789019", "file": "CIK0000789019.json", "companyName": "Microsoft Corp."},
        "AMZN": {"cik": "0001018724", "file": "CIK0001018724.json", "companyName": "Amazon.com Inc."},
        "GOOGL": {"cik": "0001652044", "file": "CIK0001652044.json", "companyName": "Alphabet Inc."}
    }

    # The 'with' block is the gold standard for writing files
    try:
        with open(mappingOutputPath, "w") as f:
            json.dump(masterMap, f, indent=4)
            f.flush() # Force write to disk
        
        # Verify the file actually exists and has content
        if os.path.exists(mappingOutputPath) and os.path.getsize(mappingOutputPath) > 0:
            print(f"✅ Success: {len(masterMap)} companies mapped to {mappingOutputPath}")
        else:
            print("❌ Error: File created but is empty.")
            
    except Exception as e:
        print(f"❌ Failed to write mapping: {e}")

if __name__ == "__main__":
    generateMasterMapping()