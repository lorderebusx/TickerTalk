#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Camel face variables
const char* processedDataDir = "E:/TickerTalk/data/processed/";

void loadCompanyData(const char* ticker) {
    char filePath[256];
    sprintf(filePath, "%s%s_slim.json", processedDataDir, ticker);

    FILE *file = fopen(filePath, "r");
    if (!file) {
        printf("Could not find data for %s\n", ticker);
        return;
    }

    printf("Successfully opened slim data for: %s\n", ticker);
    
    // In the next step, we will add a JSON parser here to serve it to the web
    fclose(file);
}

int main() {
    printf("TickerTalk Backend Initializing...\n");
    loadCompanyData("AAPL");
    return 0;
}