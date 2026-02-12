# Lab 04: Implementation of Chord Algorithm

## Introduction
This lab provides the concepts of Chord algorithm using Python simulation. The Chord protocol is a fundamental distributed hash table (DHT) algorithm used in peer-to-peer networks.

## Objectives
- To understand the concept of Chord algorithm
- To implement node joining functionality
- To implement stabilization when nodes leave the network
- To understand distributed hash tables and key-value storage

## Tools/Software Requirement
- Python 3.x
- Any Python IDE (VS Code, PyCharm, IDLE, etc.)

## Description

### What is Chord?
Chord is a protocol and algorithm for a peer-to-peer distributed hash table. A distributed hash table stores key-value pairs by assigning keys to different computers (known as "nodes"). A node stores the values for all keys for which it is responsible.

### Key Concepts
1. **Ring Structure**: Nodes are arranged in a circular ring based on their identifiers
2. **Consistent Hashing**: Keys are mapped to nodes using consistent hashing
3. **Finger Table**: Each node maintains a routing table for efficient lookups (O(log N))
4. **Successor/Predecessor**: Each node knows its immediate neighbors in the ring
5. **Join Protocol**: New nodes can join the network dynamically
6. **Stabilization**: Periodic protocol to maintain correct ring structure
7. **Key Migration**: Keys are transferred when nodes join or leave

### Algorithm Features

#### 1. **Node Join**
- New node contacts any existing node in the network
- Initializes finger table using existing node
- Updates other nodes' finger tables
- Transfers appropriate keys from successor

#### 2. **Stabilization**
- Periodically run to maintain ring consistency
- Updates successor and predecessor pointers
- Fixes finger table entries
- Handles failures gracefully

#### 3. **Node Departure**
- Transfers all keys to successor
- Updates predecessor's successor pointer
- Updates successor's predecessor pointer
- Maintains data availability

## Implementation Files

### 1. ChordNode.py
Core implementation of the Chord protocol containing:
- `ChordNode` class with all Chord operations
- **Join function**: `join(existing_node)` - Allows a node to join the network
- **Stabilization functions**: 
  - `stabilize()` - Maintains ring consistency
  - `notify(node)` - Updates predecessor information
  - `fix_fingers()` - Updates finger table entries
  - `check_predecessor()` - Verifies predecessor is alive
- **Leave function**: `leave()` - Gracefully exits the network
- **Data operations**: `put(key, value)` and `get(key)` for key-value storage
- **Lookup**: `find_successor(key)` - Finds responsible node for a key

### 2. ChordSimulation.py
Comprehensive simulation demonstrating:
- **Demo 1**: Basic Chord network creation and operations
- **Demo 2**: Key storage and retrieval across nodes
- **Demo 3**: Dynamic node joining and key redistribution
- **Demo 4**: Node departure and recovery
- **Demo 5**: Complete scenario with all operations

### 3. README.md
This documentation file

## How to Run

### Running the Full Simulation
```bash
python ChordSimulation.py
```

This will run all 5 demonstrations sequentially, showing:
1. Basic network operations
2. Key storage and retrieval
3. Node joining behavior
4. Node leaving and stabilization  
5. Complete real-world scenario

### Custom Usage Example
```python
from ChordNode import ChordNode
from ChordSimulation import ChordNetwork

# Create a Chord network (8-bit identifier space: 0-255)
network = ChordNetwork(m=8)

# Add nodes to the network
network.add_node(10)
network.add_node(50)
network.add_node(100)
network.add_node(150)

# Stabilize the network
network.stabilize_network(rounds=2)

# Store data
node = network.nodes[10]
node.put("myfile.txt", "Hello, Chord!")

# Retrieve data from any node
value = network.nodes[100].get("myfile.txt")
print(value)  # Output: Hello, Chord!

# Visualize the ring
network.visualize_ring()

# Add a new node (demonstrates join)
network.add_node(75)
network.stabilize_network(rounds=2)

# Remove a node (demonstrates leave)
network.remove_node(50)
network.stabilize_network(rounds=2)

# Display network status
network.print_network_status()
```

## Code Structure

### ChordNode Class Methods

#### Initialization
- `__init__(node_id, m)` - Create a node with given ID and identifier space

#### Core Chord Operations
- `join(existing_node)` - Join the Chord network
- `leave()` - Leave the network gracefully
- `find_successor(key)` - Find the node responsible for a key
- `closest_preceding_node(key)` - Find closest node in finger table

#### Stabilization Protocol
- `stabilize()` - Main stabilization routine
- `notify(node)` - Notification from potential predecessor
- `check_predecessor()` - Verify predecessor is alive
- `fix_fingers()` - Update finger table entries

#### Finger Table Management
- `init_finger_table(existing_node)` - Initialize finger table on join
- `update_finger_table(s, i)` - Update finger table entry
- `update_others()` - Update other nodes' finger tables

#### Data Operations
- `put(key, value)` - Store a key-value pair
- `get(key)` - Retrieve a value
- `transfer_keys()` - Transfer keys during join/leave

#### Utility Functions
- `in_range(key, start, end)` - Check if key is in range (handles wrap-around)
- `hash_key(key)` - Hash a key to the identifier space
- `print_info()` - Display node information

## Understanding the Output

### Node Information Display
```
==================================================
Node 50 Information:
==================================================
Predecessor: 10
Successor: 100

Finger Table:
  finger[0]: start= 51, node=100
  finger[1]: start= 52, node=100
  finger[2]: start= 54, node=100
  ...

Stored Keys: 2
  'file1.txt' (hash=75) = 'Content of file 1'
  'file2.txt' (hash=45) = 'Content of file 2'
==================================================
```

### Ring Visualization
```
==================================================
CHORD RING VISUALIZATION
==================================================

Ring structure (clockwise):
  [10] -> successor: 50, predecessor: 150
   |
   v
  [50] -> successor: 100, predecessor: 10
   |
   v
  [100] -> successor: 150, predecessor: 50
   |
   v
  [150] -> successor: 10, predecessor: 100
   |
   +---> (wraps back to 10)
==================================================
```

## Key Features Demonstrated

### 1. Join Function
When a node joins:
- Contact existing node
- Initialize finger table
- Update other nodes' finger tables
- Transfer keys from successor
- Stabilization ensures consistency

### 2. Stabilization
Periodic stabilization:
- Verifies successor/predecessor pointers
- Updates finger tables
- Handles concurrent joins
- Recovers from failures

### 3. Node Departure
When a node leaves:
- Transfers all keys to successor
- Updates predecessor and successor
- Network remains operational
- No data loss

### 4. Key Distribution
- Keys are hashed to identifier space
- Each node responsible for keys between predecessor and itself
- Efficient lookup using finger tables (O(log N))
- Keys automatically redistributed on join/leave

## Technical Details

### Identifier Space
- Default: m=8 bits (0-255 identifiers)
- Can be adjusted for larger networks
- Uses SHA-1 hashing modulo 2^m

### Finger Table
- Each node maintains m entries
- finger[i] points to successor of (n + 2^i) mod 2^m
- Enables O(log N) lookups
- Updated during stabilization

### Complexity
- **Lookup**: O(log N) hops
- **Join**: O(log^2 N) messages
- **Stabilization**: O(log N) per node

## Lab Tasks

### Basic Tasks
1. ✅ Run the simulation and observe the output
2. ✅ Understand how nodes join the network
3. ✅ Observe stabilization protocol in action
4. ✅ See how keys are distributed

### Advanced Tasks
1. Modify the simulation to use different identifier space sizes (m=4, m=10)
2. Add more nodes and observe scalability
3. Implement failure detection (simulated node crashes)
4. Add metrics collection (hop count, lookup time)
5. Visualize the finger tables graphically
6. Implement key replication for fault tolerance

## Expected Learning Outcomes

After completing this lab, you should be able to:
1. Explain how Chord protocol works
2. Understand distributed hash tables
3. Implement node join and leave operations
4. Understand and implement stabilization protocols
5. Manage distributed key-value storage
6. Handle dynamic network membership

## Common Issues and Solutions

### Issue 1: Keys not found after node join
**Solution**: Run stabilization to update pointers and transfer keys

### Issue 2: Ring structure broken
**Solution**: Multiple stabilization rounds fix temporary inconsistencies

### Issue 3: Keys lost after node departure
**Solution**: The leave() function transfers keys to successor before exiting

## References

1. Stoica, I., et al. (2001). "Chord: A Scalable Peer-to-peer Lookup Service for Internet Applications"
2. Original Chord paper: https://pdos.csail.mit.edu/papers/chord:sigcomm01/
3. Distributed Systems: Principles and Paradigms by Andrew S. Tanenbaum

## Assignment Questions

1. What is the time complexity of a lookup operation in Chord?
2. How does the finger table enable efficient routing?
3. What happens if multiple nodes join simultaneously?
4. How does Chord handle node failures?
5. What is the purpose of the stabilization protocol?

## Submission Requirements

1. Working code implementation (ChordNode.py and ChordSimulation.py)
2. Screenshots of simulation output
3. Report explaining the algorithm and observations
4. Analysis of lookup complexity
5. Discussion of at least one advanced task attempted

---

**Lab Created by:** GitHub Copilot  
**Date:** February 12, 2026  
**Course:** Parallel & Distributed Computing
