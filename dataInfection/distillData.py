import json
import os

sourceDir = "F:/companyfacts/"
mappingPath = "E:/TickerTalk/data/masterMapping.json"
outputDir = "E:/TickerTalk/data/processed/"

def distillCompanyFacts():
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # Robust check for the mapping file
    if not os.path.exists(mappingPath) or os.stat(mappingPath).st_size == 0:
        print(f"Error: {mappingPath} is missing or empty. Please run createMapping.py first.")
        return

    with open(mappingPath, 'r') as f:
        try:
            masterMapping = json.load(f)
        except json.JSONDecodeError:
            print(f"Error: {mappingPath} contains invalid JSON.")
            return

    for ticker, info in masterMapping.items():
        sourceFile = os.path.join(sourceDir, info['file'])
        
        if not os.path.exists(sourceFile):
            print(f"Skipping {ticker}: Source file not found in F:/")
            continue

        with open(sourceFile, 'r') as f:
            try:
                fullData = json.load(f)
                # ... (rest of your extraction logic)
                print(f"Successfully processed {ticker}")
            except json.JSONDecodeError:
                print(f"Error: Raw SEC file for {ticker} is malformed or empty.")
                continue

if __name__ == "__main__":
    distillCompanyFacts()