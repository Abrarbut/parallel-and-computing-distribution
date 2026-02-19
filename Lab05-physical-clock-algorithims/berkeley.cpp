#include <iostream>
#include <vector>
#include <ctime>
#include <cstdlib>

using namespace std;

int main() {

    cout << "===== BERKELEY ALGORITHM =====\n\n";

    const int NUM_SLAVES = 6;

    // Master clock time
    time_t master_time = time(0);

    cout << "Master Initial Time: " << ctime(&master_time) << endl;

    vector<time_t> slave_times;
    vector<long> time_differences;

    // Generate slave times (simulate different clocks)
    for (int i = 0; i < NUM_SLAVES; i++) {

        // Each slave clock differs by random ±5 seconds
        int offset = (rand() % 11) - 5;
        time_t slave_time = master_time + offset;

        slave_times.push_back(slave_time);

        cout << "Slave " << i + 1 << " Time: " << ctime(&slave_time);

        long difference = master_time - slave_time;
        time_differences.push_back(difference);

        cout << "Time Difference (Master - Slave " << i + 1 << "): "
             << difference << " seconds\n\n";
    }

    // Calculate average time difference
    long sum = 0;
    for (int i = 0; i < NUM_SLAVES; i++) {
        sum += time_differences[i];
    }

    long average_difference = sum / NUM_SLAVES;

    cout << "Average Time Difference: "
         << average_difference << " seconds\n\n";

    // Calculate synchronized time
    time_t synchronized_time = master_time + average_difference;

    cout << "Synchronized Master Time: "
         << ctime(&synchronized_time) << endl;

    cout << "Updated Slave Times:\n\n";

    // Update all slave clocks
    for (int i = 0; i < NUM_SLAVES; i++) {

        slave_times[i] += average_difference;

        cout << "Slave " << i + 1 << " New Time: "
             << ctime(&slave_times[i]);
    }

    return 0;
}
