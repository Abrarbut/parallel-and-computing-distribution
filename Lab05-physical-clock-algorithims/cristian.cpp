#include <iostream>
#include <chrono>
#include <thread>

using namespace std;
using namespace std::chrono;

int main() {

    cout << "===== CRISTIAN'S ALGORITHM =====\n\n";

    // Step 1: Client sends request at time T0
    auto T0 = system_clock::now();

    // Simulate network delay (100 ms)
    this_thread::sleep_for(milliseconds(100));

    // Step 2: Server sends its current time
    auto T_server = system_clock::now();

    // Simulate response delay (100 ms)
    this_thread::sleep_for(milliseconds(100));

    // Step 3: Client receives response at time T1
    auto T1 = system_clock::now();

    // Calculate Round Trip Time
    auto RTT = duration_cast<milliseconds>(T1 - T0).count();

    // Calculate synchronized client time
    auto synchronized_time = T_server + milliseconds(RTT / 2);

    // Convert to readable format
    time_t server_time = system_clock::to_time_t(T_server);
    time_t client_actual = system_clock::to_time_t(T1);
    time_t client_sync = system_clock::to_time_t(synchronized_time);

    cout << "Server Time: " << ctime(&server_time);
    cout << "Client Actual Time: " << ctime(&client_actual);
    cout << "Round Trip Time (RTT): " << RTT << " ms\n";
    cout << "Synchronized Client Time: " << ctime(&client_sync);

    return 0;
}
