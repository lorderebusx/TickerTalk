#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock2.h> // Windows Socket Library

// Camel face constants
#define PORT 8080
#define BUFFER_SIZE 4096
const char* processedDataDir = "E:/TickerTalk/data/processed/";

// Helper to read file content
char* readFile(const char* filename) {
    FILE *f = fopen(filename, "rb");
    if (!f) return NULL;
    
    fseek(f, 0, SEEK_END);
    long length = ftell(f);
    fseek(f, 0, SEEK_SET);
    
    char *buffer = malloc(length + 1);
    if (buffer) {
        fread(buffer, 1, length, f);
        buffer[length] = '\0';
    }
    fclose(f);
    return buffer;
}

int main() {
    WSADATA wsaData;
    SOCKET serverSocket, clientSocket;
    struct sockaddr_in serverAddr, clientAddr;
    int addrLen = sizeof(clientAddr);
    char buffer[BUFFER_SIZE];

    // 1. Initialize Winsock
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        printf("Failed to initialize Winsock.\n");
        return 1;
    }

    // 2. Create Socket
    serverSocket = socket(AF_INET, SOCK_STREAM, 0);
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    serverAddr.sin_port = htons(PORT);

    // 3. Bind & Listen
    bind(serverSocket, (struct sockaddr *)&serverAddr, sizeof(serverAddr));
    listen(serverSocket, 3);
    printf("🚀 TickerTalk Server running on http://localhost:%d\n", PORT);

    while (1) {
        clientSocket = accept(serverSocket, (struct sockaddr *)&clientAddr, &addrLen);
        if (clientSocket == INVALID_SOCKET) continue;

        // 4. Read Request
        int bytesRead = recv(clientSocket, buffer, BUFFER_SIZE - 1, 0);
        buffer[bytesRead] = '\0';

        // simple parsing: GET /AAPL HTTP/1.1
        char method[10], route[100];
        sscanf(buffer, "%s %s", method, route);

        printf("Request: %s %s\n", method, route);

        // 5. Route Handling
        char *responseBody = NULL;
        char header[1024];

        // Clean route string (remove leading slash)
        char *ticker = route + 1; 
        
        // Construct file path: E:/TickerTalk/data/processed/AAPL_slim.json
        char filePath[256];
        sprintf(filePath, "%s%s_slim.json", processedDataDir, ticker);
        
        responseBody = readFile(filePath);

        if (responseBody) {
            // 200 OK
            sprintf(header, 
                "HTTP/1.1 200 OK\r\n"
                "Content-Type: application/json\r\n"
                "Access-Control-Allow-Origin: *\r\n" // Important for JS fetch
                "Content-Length: %llu\r\n\r\n", 
                strlen(responseBody));
            send(clientSocket, header, strlen(header), 0);
            send(clientSocket, responseBody, strlen(responseBody), 0);
            free(responseBody);
        } else {
            // 404 Not Found
            char *errorMsg = "{\"error\": \"Ticker not found\"}";
            sprintf(header, 
                "HTTP/1.1 404 Not Found\r\n"
                "Content-Type: application/json\r\n"
                "Access-Control-Allow-Origin: *\r\n"
                "Content-Length: %llu\r\n\r\n", 
                strlen(errorMsg));
            send(clientSocket, header, strlen(header), 0);
            send(clientSocket, errorMsg, strlen(errorMsg), 0);
        }

        closesocket(clientSocket);
    }

    WSACleanup();
    return 0;
}