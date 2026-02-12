"""
Chord Algorithm Simulation
This script demonstrates the Chord DHT protocol including:
- Node joining
- Finger table construction
- Key lookup
- Stabilization
- Node departure
"""

from ChordNode import ChordNode
import time


class ChordNetwork:
    """
    Manages the entire Chord network and provides utilities for simulation.
    """
    
    def __init__(self, m=8):
        """
        Initialize Chord network.
        
        Args:
            m: Number of bits for identifier space (2^m nodes possible)
        """
        self.m = m
        self.nodes = {}  # Dictionary of active nodes: {node_id: ChordNode}
        
    def add_node(self, node_id):
        """
        Add a new node to the network.
        """
        if node_id in self.nodes:
            print(f"Node {node_id} already exists!")
            return None
        
        new_node = ChordNode(node_id, self.m)
        
        if not self.nodes:
            # First node - creates the network
            new_node.join(None)
        else:
            # Join through any existing node
            existing_node = list(self.nodes.values())[0]
            new_node.join(existing_node)
        
        self.nodes[node_id] = new_node
        return new_node
    
    def remove_node(self, node_id):
        """
        Remove a node from the network.
        """
        if node_id not in self.nodes:
            print(f"Node {node_id} does not exist!")
            return
        
        node = self.nodes[node_id]
        node.leave()
        del self.nodes[node_id]
    
    def stabilize_network(self, rounds=3):
        """
        Run stabilization protocol across all nodes.
        """
        print(f"\n{'='*60}")
        print(f"Running Stabilization ({rounds} rounds)")
        print(f"{'='*60}")
        
        for round_num in range(rounds):
            print(f"\n--- Stabilization Round {round_num + 1} ---")
            for node in self.nodes.values():
                node.stabilize()
                node.check_predecessor()
                node.fix_fingers()
    
    def print_network_status(self):
        """
        Display the current state of the entire network.
        """
        print(f"\n{'#'*60}")
        print(f"CHORD NETWORK STATUS")
        print(f"{'#'*60}")
        print(f"Total Nodes: {len(self.nodes)}")
        print(f"Node IDs: {sorted(self.nodes.keys())}")
        
        for node_id in sorted(self.nodes.keys()):
            self.nodes[node_id].print_info()
    
    def visualize_ring(self):
        """
        Simple text visualization of the Chord ring.
        """
        if not self.nodes:
            print("Network is empty!")
            return
        
        print(f"\n{'='*60}")
        print("CHORD RING VISUALIZATION")
        print(f"{'='*60}")
        
        sorted_ids = sorted(self.nodes.keys())
        print("\nRing structure (clockwise):")
        for i, node_id in enumerate(sorted_ids):
            node = self.nodes[node_id]
            successor_id = node.successor.id if node.successor else "None"
            predecessor_id = node.predecessor.id if node.predecessor else "None"
            
            print(f"  [{node_id}] -> successor: {successor_id}, predecessor: {predecessor_id}")
            
            if i < len(sorted_ids) - 1:
                print("   |")
                print("   v")
        
        print(f"   |")
        print(f"   +---> (wraps back to {sorted_ids[0]})")
        print(f"{'='*60}\n")


def demo_basic_chord():
    """
    Demonstration 1: Basic Chord operations
    """
    print("\n" + "="*70)
    print(" DEMONSTRATION 1: BASIC CHORD NETWORK ")
    print("="*70)
    
    # Create network with 8-bit identifier space (0-255)
    network = ChordNetwork(m=8)
    
    # Add first node
    print("\n### Step 1: Creating first node (Node 0) ###")
    network.add_node(0)
    
    # Add more nodes
    print("\n### Step 2: Adding Node 50 ###")
    network.add_node(50)
    
    print("\n### Step 3: Adding Node 100 ###")
    network.add_node(100)
    
    print("\n### Step 4: Adding Node 150 ###")
    network.add_node(150)
    
    # Visualize the ring
    network.visualize_ring()
    
    # Run stabilization
    network.stabilize_network(rounds=2)
    
    # Display network status
    network.print_network_status()
    
    return network


def demo_key_storage():
    """
    Demonstration 2: Key storage and retrieval
    """
    print("\n" + "="*70)
    print(" DEMONSTRATION 2: KEY STORAGE AND RETRIEVAL ")
    print("="*70)
    
    # Create network
    network = ChordNetwork(m=8)
    
    # Add nodes
    print("\n### Creating network with nodes: 10, 30, 60, 120, 200 ###")
    network.add_node(10)
    network.add_node(30)
    network.add_node(60)
    network.add_node(120)
    network.add_node(200)
    
    # Stabilize
    network.stabilize_network(rounds=2)
    
    # Store some keys
    print("\n### Storing key-value pairs ###")
    node = network.nodes[10]
    node.put("file1.txt", "Content of file 1")
    node.put("file2.txt", "Content of file 2")
    node.put("database.db", "Database contents")
    node.put("config.ini", "Configuration data")
    node.put("image.png", "Image data")
    
    # Retrieve keys from different nodes
    print("\n### Retrieving keys from different nodes ###")
    network.nodes[120].get("file1.txt")
    network.nodes[200].get("database.db")
    network.nodes[30].get("config.ini")
    
    # Show which node stores which keys
    print("\n### Key distribution across nodes ###")
    for node_id in sorted(network.nodes.keys()):
        node = network.nodes[node_id]
        if node.data:
            print(f"Node {node_id} stores: {list(node.data.keys())}")
    
    return network


def demo_node_join():
    """
    Demonstration 3: Dynamic node joining
    """
    print("\n" + "="*70)
    print(" DEMONSTRATION 3: DYNAMIC NODE JOINING ")
    print("="*70)
    
    # Start with small network
    network = ChordNetwork(m=8)
    
    print("\n### Initial network: Nodes 0, 50, 100 ###")
    network.add_node(0)
    network.add_node(50)
    network.add_node(100)
    
    network.stabilize_network(rounds=1)
    network.visualize_ring()
    
    # Store some data
    print("\n### Storing data before new node joins ###")
    network.nodes[0].put("key1", "value1")
    network.nodes[0].put("key2", "value2")
    network.nodes[0].put("key3", "value3")
    
    # Add new node in the middle
    print("\n### New node (Node 75) joining between Node 50 and Node 100 ###")
    network.add_node(75)
    
    network.stabilize_network(rounds=2)
    network.visualize_ring()
    
    # Check key distribution after join
    print("\n### Key distribution after node join ###")
    for node_id in sorted(network.nodes.keys()):
        node = network.nodes[node_id]
        if node.data:
            print(f"Node {node_id} stores: {list(node.data.keys())}")
    
    return network


def demo_node_leave():
    """
    Demonstration 4: Node departure and stabilization
    """
    print("\n" + "="*70)
    print(" DEMONSTRATION 4: NODE DEPARTURE AND RECOVERY ")
    print("="*70)
    
    # Create network
    network = ChordNetwork(m=8)
    
    print("\n### Creating network with 5 nodes ###")
    for node_id in [10, 40, 80, 120, 200]:
        network.add_node(node_id)
    
    network.stabilize_network(rounds=2)
    
    # Store data
    print("\n### Storing data in the network ###")
    network.nodes[10].put("important_file.txt", "Critical data")
    network.nodes[10].put("backup.zip", "Backup data")
    network.nodes[10].put("log.txt", "Log entries")
    
    print("\n### Before node departure ###")
    network.visualize_ring()
    
    # Show data distribution
    print("\n### Data distribution before node leaves ###")
    for node_id in sorted(network.nodes.keys()):
        node = network.nodes[node_id]
        if node.data:
            print(f"Node {node_id} stores: {list(node.data.keys())}")
    
    # Remove a node
    print("\n### Node 80 is leaving the network ###")
    network.remove_node(80)
    
    # Stabilize after departure
    network.stabilize_network(rounds=2)
    
    print("\n### After node departure ###")
    network.visualize_ring()
    
    # Verify data is still accessible
    print("\n### Verifying data integrity after node departure ###")
    network.nodes[10].get("important_file.txt")
    network.nodes[40].get("backup.zip")
    network.nodes[120].get("log.txt")
    
    print("\n### Data distribution after node leaves ###")
    for node_id in sorted(network.nodes.keys()):
        node = network.nodes[node_id]
        if node.data:
            print(f"Node {node_id} stores: {list(node.data.keys())}")
    
    return network


def demo_complete_scenario():
    """
    Demonstration 5: Complete scenario with multiple operations
    """
    print("\n" + "="*70)
    print(" DEMONSTRATION 5: COMPLETE CHORD SCENARIO ")
    print("="*70)
    
    # Create network
    network = ChordNetwork(m=6)  # Smaller space for easier visualization
    
    print("\n### Phase 1: Building the network ###")
    for node_id in [5, 15, 25, 40, 50]:
        network.add_node(node_id)
        network.stabilize_network(rounds=1)
    
    network.visualize_ring()
    
    print("\n### Phase 2: Storing data ###")
    network.nodes[5].put("user1.profile", "User 1 data")
    network.nodes[5].put("user2.profile", "User 2 data")
    network.nodes[15].put("session.token", "Session data")
    network.nodes[25].put("cache.data", "Cached content")
    
    print("\n### Phase 3: Adding new nodes ###")
    network.add_node(10)
    network.add_node(35)
    network.stabilize_network(rounds=2)
    
    network.visualize_ring()
    
    print("\n### Phase 4: Removing a node ###")
    network.remove_node(25)
    network.stabilize_network(rounds=2)
    
    print("\n### Phase 5: Final network state ###")
    network.print_network_status()
    
    return network


def main():
    """
    Main function to run all demonstrations
    """
    print("#" * 70)
    print("#" + " " * 68 + "#")
    print("#" + " " * 15 + "CHORD ALGORITHM SIMULATION" + " " * 27 + "#")
    print("#" + " " * 68 + "#")
    print("#" * 70)
    
    # Run demonstrations
    try:
        # Demo 1: Basic operations
        demo_basic_chord()
        input("\nPress Enter to continue to next demonstration...")
        
        # Demo 2: Key storage
        demo_key_storage()
        input("\nPress Enter to continue to next demonstration...")
        
        # Demo 3: Node joining
        demo_node_join()
        input("\nPress Enter to continue to next demonstration...")
        
        # Demo 4: Node leaving
        demo_node_leave()
        input("\nPress Enter to continue to next demonstration...")
        
        # Demo 5: Complete scenario
        demo_complete_scenario()
        
        print("\n" + "="*70)
        print(" SIMULATION COMPLETE ")
        print("="*70)
        
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user.")
    except Exception as e:
        print(f"\nError occurred: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
