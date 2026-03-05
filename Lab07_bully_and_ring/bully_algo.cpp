#include <iostream>
using namespace std;

#define MAX_PROCESSES 7

struct Process {
    int  id;
    int  priority;
    bool active;   // true = active (1), false = inactive (0)
};

Process procs[MAX_PROCESSES];

// ── Initialize 7 processes with unique priorities ──────────────────────
void initProcesses() {
    int priorities[MAX_PROCESSES] = {4, 7, 2, 9, 1, 6, 3};
    for (int i = 0; i < MAX_PROCESSES; i++) {
        procs[i].id       = i + 1;
        procs[i].priority = priorities[i];
        procs[i].active   = true;
    }
}

// ── Print current state of all processes ──────────────────────────────
void printState() {
    cout << "\nProcess States:" << endl;
    cout << "+---------+----------+--------+" << endl;
    cout << "| Process | Priority | Status |" << endl;
    cout << "+---------+----------+--------+" << endl;
    for (int i = 0; i < MAX_PROCESSES; i++) {
        cout << "|   P" << procs[i].id
             << "    |    " << procs[i].priority
             << "     |   " << (procs[i].active ? "1" : "0")
             << "    |" << endl;
    }
    cout << "+---------+----------+--------+" << endl;
}

// ── Run Bully Election from initiator processIndex ────────────────────
int bullyElection(int initiatorIndex) {
    cout << "\n>> Process P" << procs[initiatorIndex].id
         << " (priority=" << procs[initiatorIndex].priority
         << ") initiates election." << endl;

    int highestPriority = -1;
    int coordinatorIdx  = -1;
    bool higherExists   = false;

    for (int i = 0; i < MAX_PROCESSES; i++) {
        if (procs[i].active &&
            procs[i].priority > procs[initiatorIndex].priority) {
            cout << "   P" << procs[initiatorIndex].id
                 << " sends ELECTION to P" << procs[i].id << endl;
            higherExists = true;
            if (procs[i].priority > highestPriority) {
                highestPriority = procs[i].priority;
                coordinatorIdx  = i;
            }
        }
    }

    if (!higherExists) {
        coordinatorIdx = initiatorIndex;
        cout << "   No response. P" << procs[coordinatorIdx].id
             << " elects itself." << endl;
    } else {
        cout << "   P" << procs[coordinatorIdx].id
             << " (priority=" << highestPriority
             << ") wins and becomes coordinator." << endl;
    }

    cout << "\n>> P" << procs[coordinatorIdx].id
         << " broadcasts COORDINATOR message." << endl;
    for (int i = 0; i < MAX_PROCESSES; i++) {
        if (procs[i].active && i != coordinatorIdx)
            cout << "   P" << procs[coordinatorIdx].id
                 << " -> P" << procs[i].id << " : COORDINATOR" << endl;
    }

    cout << "\n==> COORDINATOR elected: P"
         << procs[coordinatorIdx].id
         << " (priority=" << procs[coordinatorIdx].priority << ")"
         << endl;

    return coordinatorIdx;
}

int main() {
    cout << "==========================================" << endl;
    cout << "  Bully Algorithm -- 7 Processes          " << endl;
    cout << "==========================================" << endl;

    initProcesses();
    printState();

    // Round 1: Process P3 (index 2) initiates election
    cout << "\n--- ROUND 1: Process P3 initiates election ---" << endl;
    int coordinator = bullyElection(2);

    // Coordinator fails
    cout << "\n>> Coordinator P" << procs[coordinator].id
         << " has FAILED. Setting inactive." << endl;
    procs[coordinator].active = false;

    printState();

    // Round 2: P3 initiates again among 6 remaining processes
    cout << "\n--- ROUND 2: Process P3 initiates election "
         << "(6 remaining processes) ---" << endl;
    bullyElection(2);

    cout << "\n==========================================" << endl;
    cout << "  Simulation Complete" << endl;
    cout << "==========================================" << endl;

    return 0;
}