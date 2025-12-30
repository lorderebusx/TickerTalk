import json
import os

# Camel face paths
sourceDir = "F:/companyfacts/"
mappingPath = "E:/TickerTalk/data/masterMapping.json"
outputDir = "E:/TickerTalk/data/processed/"

# 1. The Tag Hunter Logic
def getFinancialValue(gaapData, possibleTags):
    """
    Hunts through a list of possible US-GAAP tags.
    Returns the first list of data it finds.
    """
    for tag in possibleTags:
        if tag in gaapData:
            # We found a match! Return the 'USD' unit list
            return gaapData[tag].get('units', {}).get('USD', [])
    return []

def distillCompanyFacts():
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)

    # Load the mapping
    with open(mappingPath, 'r') as f:
        masterMapping = json.load(f)

    # 2. Define the 'Hunt List' for 2025
    # UPDATE THIS LIST IN distillData.py
    revenueTags = [
        'RevenueFromContractWithCustomerExcludingAssessedTax', # <--- Put this FIRST
        'Revenues', 
        'SalesRevenueNet', 
        'RevenuesNetOfInterestExpense'
    ]
    
    incomeTags = [
        'NetIncomeLoss', 
        'NetIncomeLossAvailableToCommonStockholdersBasic', 
        'ProfitLoss'
    ]

    print(f"Starting distillation for {len(masterMapping)} companies...")

    for ticker, info in masterMapping.items():
        sourceFile = os.path.join(sourceDir, info['file'])
        
        # Skip if raw file doesn't exist
        if not os.path.exists(sourceFile):
            print(f"Skipping {ticker}: Raw file not found.")
            continue

        try:
            with open(sourceFile, 'r') as f:
                fullData = json.load(f)
            
            gaapFacts = fullData.get('facts', {}).get('us-gaap', {})
            
            # 3. Use the Hunter to find data
            revenueData = getFinancialValue(gaapFacts, revenueTags)
            incomeData = getFinancialValue(gaapFacts, incomeTags)

            slimData = {
                "ticker": ticker,
                "companyName": info['companyName'],
                "fiscalHistory": []
            }

            # 4. Extract only Annual (FY) data
            # We use a dictionary to merge Revenue and Income by Year
            historyMap = {}

            for entry in revenueData:
                if entry.get('fp') == 'FY':
                    year = entry['fy']
                    if year not in historyMap: historyMap[year] = {}
                    historyMap[year]['revenue'] = entry['val']

            for entry in incomeData:
                if entry.get('fp') == 'FY':
                    year = entry['fy']
                    if year in historyMap: # Only add if we already have revenue entry
                        historyMap[year]['netIncome'] = entry['val']

            # Convert map to clean list
            for year, data in sorted(historyMap.items()):
                if 'revenue' in data and 'netIncome' in data:
                    slimData['fiscalHistory'].append({
                        "year": year,
                        "revenue": data['revenue'],
                        "netIncome": data['netIncome']
                    })

            # Save Slim JSON
            outputFile = os.path.join(outputDir, f"{ticker}_slim.json")
            with open(outputFile, 'w') as out:
                json.dump(slimData, out, indent=4)
                
            print(f"✅ Distilled {ticker} ({len(slimData['fiscalHistory'])} years of data)")

        except Exception as e:
            print(f"❌ Error processing {ticker}: {e}")

if __name__ == "__main__":
    distillCompanyFacts()