#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;

#define MAX_PROCESSES 7

struct Process {
    int  id;
    int  priority;
    bool active;
};

Process procs[MAX_PROCESSES];

// ── Initialize 7 processes ────────────────────────────────────────────
void initProcesses() {
    int priorities[MAX_PROCESSES] = {4, 7, 2, 9, 1, 6, 3};
    for (int i = 0; i < MAX_PROCESSES; i++) {
        procs[i].id       = i + 1;
        procs[i].priority = priorities[i];
        procs[i].active   = true;
    }
}

// ── Print current state ───────────────────────────────────────────────
void printState() {
    cout << "\nProcess States (Ring: P1->P2->...->P7->P1):" << endl;
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

// ── Get next active process index clockwise ───────────────────────────
int nextActive(int current) {
    int next = (current + 1) % MAX_PROCESSES;
    while (!procs[next].active && next != current)
        next = (next + 1) % MAX_PROCESSES;
    return next;
}

// ── Run Ring Election from initiator processIndex ─────────────────────
int ringElection(int initiatorIndex) {
    cout << "\n>> Process P" << procs[initiatorIndex].id
         << " (priority=" << procs[initiatorIndex].priority
         << ") initiates election." << endl;

    vector<int> activeList;
    activeList.push_back(procs[initiatorIndex].priority);

    int current = nextActive(initiatorIndex);

    while (current != initiatorIndex) {
        if (procs[current].active) {
            activeList.push_back(procs[current].priority);
            cout << "   ELECTION passes through P" << procs[current].id
                 << "  active_list: [";
            for (size_t k = 0; k < activeList.size(); k++) {
                cout << activeList[k];
                if (k < activeList.size() - 1) cout << ", ";
            }
            cout << "]" << endl;
        }
        current = nextActive(current);
    }

    cout << "\n>> P" << procs[initiatorIndex].id
         << " received its own message back. List: [";
    for (size_t k = 0; k < activeList.size(); k++) {
        cout << activeList[k];
        if (k < activeList.size() - 1) cout << ", ";
    }
    cout << "]" << endl;

    int maxPriority    = *max_element(activeList.begin(), activeList.end());
    int coordinatorIdx = -1;
    for (int i = 0; i < MAX_PROCESSES; i++) {
        if (procs[i].active && procs[i].priority == maxPriority) {
            coordinatorIdx = i;
            break;
        }
    }

    cout << "\n>> P" << procs[initiatorIndex].id
         << " broadcasts COORDINATOR: P"
         << procs[coordinatorIdx].id << endl;

    cout << "\n==> COORDINATOR elected: P"
         << procs[coordinatorIdx].id
         << " (priority=" << procs[coordinatorIdx].priority << ")"
         << endl;

    return coordinatorIdx;
}

int main() {
    cout << "==========================================" << endl;
    cout << "  Ring Algorithm -- 7 Processes           " << endl;
    cout << "==========================================" << endl;

    initProcesses();
    printState();

    // Round 1: P3 (index 2) initiates election
    cout << "\n--- ROUND 1: Process P3 initiates election ---" << endl;
    int coordinator = ringElection(2);

    // Coordinator fails
    cout << "\n>> Coordinator P" << procs[coordinator].id
         << " has FAILED. Setting inactive." << endl;
    procs[coordinator].active = false;

    printState();

    // Round 2: P3 initiates again among 6 remaining
    cout << "\n--- ROUND 2: P3 initiates election "
         << "(6 remaining processes) ---" << endl;
    ringElection(2);

    cout << "\n==========================================" << endl;
    cout << "  Simulation Complete" << endl;
    cout << "==========================================" << endl;

    return 0;
}