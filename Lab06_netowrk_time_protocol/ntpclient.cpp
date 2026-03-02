#include <iostream>
#include <string>
#include <winsock2.h>
#include <ws2tcpip.h>
#include <time.h>

#pragma comment(lib, "ws2_32.lib")

using namespace std;

typedef struct {
    unsigned char  li_vn_mode;
    unsigned char  stratum;
    unsigned char  poll;
    unsigned char  precision;
    unsigned int   root_delay;
    unsigned int   root_dispersion;
    unsigned int   ref_id;
    unsigned int   ref_ts_sec;
    unsigned int   ref_ts_frac;
    unsigned int   orig_ts_sec;
    unsigned int   orig_ts_frac;
    unsigned int   rx_ts_sec;
    unsigned int   rx_ts_frac;
    unsigned int   tx_ts_sec;
    unsigned int   tx_ts_frac;
} NTPPacket;

#define NTP_PORT 123
#define NTP_TIMESTAMP_DELTA 2208988800ULL

bool GetTimeFromNTPServer(const string& serverName)
{
    SOCKET      sock    = INVALID_SOCKET;
    addrinfo*   result  = NULL;
    bool        success = false;

    addrinfo hints;
    ZeroMemory(&hints, sizeof(hints));
    hints.ai_family   = AF_INET;
    hints.ai_socktype = SOCK_DGRAM;
    hints.ai_protocol = IPPROTO_UDP;

    char portStr[8];
    sprintf_s(portStr, "%d", NTP_PORT);

    if (getaddrinfo(serverName.c_str(), portStr, &hints, &result) != 0) {
        cerr << "[ERROR] Cannot resolve server: " << serverName << endl;
        return false;
    }

    sock = socket(result->ai_family, result->ai_socktype, result->ai_protocol);
    if (sock == INVALID_SOCKET) {
        cerr << "[ERROR] Socket creation failed." << endl;
        freeaddrinfo(result);
        return false;
    }

    DWORD timeout = 3000;
    setsockopt(sock, SOL_SOCKET, SO_RCVTIMEO, (char*)&timeout, sizeof(timeout));

    NTPPacket packet;
    ZeroMemory(&packet, sizeof(packet));
    packet.li_vn_mode = 0x1B;

    if (sendto(sock, (char*)&packet, sizeof(packet), 0,
               result->ai_addr, (int)result->ai_addrlen) == SOCKET_ERROR)
    {
        cerr << "[ERROR] Failed to send to: " << serverName << endl;
        goto cleanup;
    }

    {
        sockaddr_in fromAddr;
        int fromLen = sizeof(fromAddr);
        int received = recvfrom(sock, (char*)&packet, sizeof(packet), 0,
                                (sockaddr*)&fromAddr, &fromLen);
        if (received == SOCKET_ERROR) {
            cerr << "[ERROR] No response from: " << serverName << endl;
            goto cleanup;
        }
    }

    {
        unsigned long long txSec = ntohl(packet.tx_ts_sec);

        if (txSec < NTP_TIMESTAMP_DELTA) {
            cerr << "[ERROR] Invalid timestamp received." << endl;
            goto cleanup;
        }
        time_t unixTime = (time_t)(txSec - NTP_TIMESTAMP_DELTA);

        struct tm tmInfo;
        gmtime_s(&tmInfo, &unixTime);

        char timeBuf[64];
        strftime(timeBuf, sizeof(timeBuf), "%Y-%m-%d  %H:%M:%S UTC", &tmInfo);

        cout << "Server : " << serverName << endl;
        cout << "Time   : " << timeBuf    << endl;
        cout << "-------------------------------------------" << endl;

        success = true;
    }

cleanup:
    closesocket(sock);
    freeaddrinfo(result);
    return success;
}

int main()
{
    WSADATA wsaData;
    if (WSAStartup(MAKEWORD(2, 2), &wsaData) != 0) {
        cerr << "WSAStartup failed." << endl;
        return 1;
    }

    cout << "=========================================" << endl;
    cout << "  Lab 06 - NTP Client (10 Servers)       " << endl;
    cout << "=========================================" << endl << endl;

    // Task 2: Query 10 NTP servers
    string servers[10] = {
        "pool.ntp.org",
        "time.google.com",
        "time.windows.com",
        "time.apple.com",
        "time.cloudflare.com",
        "0.pool.ntp.org",
        "1.pool.ntp.org",
        "2.pool.ntp.org",
        "3.pool.ntp.org",
        "ntp.ubuntu.com"
    };

    int successCount = 0;
    for (int i = 0; i < 10; i++)
    {
        cout << "[" << (i + 1) << "/10] Querying: " << servers[i] << endl;
        if (GetTimeFromNTPServer(servers[i]))
            successCount++;
    }

    cout << endl;
    cout << "=========================================" << endl;
    cout << "  Completed: " << successCount << "/10 servers responded." << endl;
    cout << "=========================================" << endl;

    WSACleanup();

    cout << endl << "Press Enter to exit...";
    cin.get();
    return 0;
}