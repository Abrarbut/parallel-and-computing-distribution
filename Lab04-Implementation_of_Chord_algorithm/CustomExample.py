"""
Custom Chord Example
A simple example showing how to use the Chord implementation
for your own experiments and testing.
"""

from ChordNode import ChordNode
from ChordSimulation import ChordNetwork


def simple_example():
    """
    Simple example demonstrating basic Chord operations.
    """
    print("="*60)
    print("SIMPLE CHORD EXAMPLE")
    print("="*60)
    
    # Create a network with 6-bit address space (0-63)
    print("\n1. Creating Chord network...")
    network = ChordNetwork(m=6)
    
    # Add some nodes
    print("\n2. Adding nodes 5, 15, 30, 45...")
    network.add_node(5)
    network.add_node(15)
    network.add_node(30)
    network.add_node(45)
    
    # Stabilize the network
    print("\n3. Running stabilization...")
    network.stabilize_network(rounds=2)
    
    # Visualize the ring
    print("\n4. Network topology:")
    network.visualize_ring()
    
    # Store some data
    print("\n5. Storing data...")
    node5 = network.nodes[5]
    node5.put("alice.txt", "Alice's document")
    node5.put("bob.txt", "Bob's document")
    node5.put("charlie.txt", "Charlie's document")
    
    # Retrieve data from different nodes
    print("\n6. Retrieving data from different nodes...")
    network.nodes[15].get("alice.txt")
    network.nodes[30].get("bob.txt")
    network.nodes[45].get("charlie.txt")
    
    # Show data distribution
    print("\n7. Data distribution:")
    for node_id in sorted(network.nodes.keys()):
        node = network.nodes[node_id]
        if node.data:
            print(f"   Node {node_id}: {list(node.data.keys())}")
    
    return network


def test_join_and_leave():
    """
    Test node joining and leaving with data transfers.
    """
    print("\n" + "="*60)
    print("TEST: NODE JOIN AND LEAVE")
    print("="*60)
    
    # Create initial network
    print("\n1. Creating initial network with nodes 10, 30, 50...")
    network = ChordNetwork(m=7)
    network.add_node(10)
    network.add_node(30)
    network.add_node(50)
    network.stabilize_network(rounds=2)
    
    # Add data
    print("\n2. Adding test data...")
    network.nodes[10].put("test1", "data1")
    network.nodes[10].put("test2", "data2")
    network.nodes[10].put("test3", "data3")
    
    print("\n3. Data before new node joins:")
    for node_id in sorted(network.nodes.keys()):
        node = network.nodes[node_id]
        if node.data:
            print(f"   Node {node_id}: {list(node.data.keys())}")
    
    # Add new node
    print("\n4. Adding new node 40...")
    network.add_node(40)
    network.stabilize_network(rounds=2)
    
    print("\n5. Data after node 40 joins:")
    for node_id in sorted(network.nodes.keys()):
        node = network.nodes[node_id]
        if node.data:
            print(f"   Node {node_id}: {list(node.data.keys())}")
    
    # Remove node
    print("\n6. Removing node 30...")
    network.remove_node(30)
    network.stabilize_network(rounds=2)
    
    print("\n7. Data after node 30 leaves:")
    for node_id in sorted(network.nodes.keys()):
        node = network.nodes[node_id]
        if node.data:
            print(f"   Node {node_id}: {list(node.data.keys())}")
    
    # Verify data is still accessible
    print("\n8. Verifying all data is still accessible:")
    network.nodes[10].get("test1")
    network.nodes[40].get("test2")
    network.nodes[50].get("test3")
    
    print("\n✓ All data successfully retrieved!")


def test_finger_tables():
    """
    Examine finger tables in detail.
    """
    print("\n" + "="*60)
    print("TEST: FINGER TABLE EXAMINATION")
    print("="*60)
    
    # Create network
    print("\n1. Creating network with nodes 0, 20, 40, 60, 80, 100...")
    network = ChordNetwork(m=7)  # 0-127
    
    for node_id in [0, 20, 40, 60, 80, 100]:
        network.add_node(node_id)
    
    network.stabilize_network(rounds=2)
    
    # Display finger tables
    print("\n2. Detailed finger table for Node 20:")
    node = network.nodes[20]
    node.print_info()


def stress_test():
    """
    Stress test with many nodes.
    """
    print("\n" + "="*60)
    print("STRESS TEST: MANY NODES")
    print("="*60)
    
    # Create network with many nodes
    print("\n1. Creating network with 20 random nodes...")
    network = ChordNetwork(m=8)
    
    import random
    nodes_to_add = random.sample(range(0, 256), 20)
    nodes_to_add.sort()
    
    print(f"   Node IDs: {nodes_to_add}")
    
    for node_id in nodes_to_add:
        network.add_node(node_id)
    
    print("\n2. Stabilizing network...")
    network.stabilize_network(rounds=3)
    
    print("\n3. Adding 50 key-value pairs...")
    for i in range(50):
        key = f"key_{i}"
        value = f"value_{i}"
        network.nodes[nodes_to_add[0]].put(key, value)
    
    print("\n4. Data distribution:")
    for node_id in sorted(network.nodes.keys()):
        node = network.nodes[node_id]
        if node.data:
            print(f"   Node {node_id}: {len(node.data)} keys")
    
    print("\n5. Testing random retrievals...")
    for i in [0, 10, 25, 35, 49]:
        key = f"key_{i}"
        random_node = random.choice(nodes_to_add)
        result = network.nodes[random_node].get(key)
        if result:
            print(f"   ✓ Successfully retrieved {key}")


def interactive_mode():
    """
    Interactive mode for experimenting with Chord.
    """
    print("\n" + "="*60)
    print("INTERACTIVE CHORD MODE")
    print("="*60)
    
    network = ChordNetwork(m=8)
    
    print("\nCommands:")
    print("  add <id>        - Add a node with given ID")
    print("  remove <id>     - Remove a node with given ID")
    print("  put <key> <val> - Store a key-value pair")
    print("  get <key>       - Retrieve a value")
    print("  show            - Show network status")
    print("  ring            - Show ring visualization")
    print("  stabilize       - Run stabilization")
    print("  node <id>       - Show detailed node info")
    print("  quit            - Exit")
    
    while True:
        try:
            command = input("\nchord> ").strip().split()
            
            if not command:
                continue
            
            cmd = command[0].lower()
            
            if cmd == "quit":
                break
            
            elif cmd == "add" and len(command) == 2:
                node_id = int(command[1])
                network.add_node(node_id)
            
            elif cmd == "remove" and len(command) == 2:
                node_id = int(command[1])
                network.remove_node(node_id)
            
            elif cmd == "put" and len(command) >= 3:
                key = command[1]
                value = " ".join(command[2:])
                if network.nodes:
                    first_node = list(network.nodes.values())[0]
                    first_node.put(key, value)
                else:
                    print("No nodes in network!")
            
            elif cmd == "get" and len(command) == 2:
                key = command[1]
                if network.nodes:
                    first_node = list(network.nodes.values())[0]
                    first_node.get(key)
                else:
                    print("No nodes in network!")
            
            elif cmd == "show":
                network.print_network_status()
            
            elif cmd == "ring":
                network.visualize_ring()
            
            elif cmd == "stabilize":
                network.stabilize_network(rounds=2)
            
            elif cmd == "node" and len(command) == 2:
                node_id = int(command[1])
                if node_id in network.nodes:
                    network.nodes[node_id].print_info()
                else:
                    print(f"Node {node_id} does not exist!")
            
            else:
                print("Invalid command!")
        
        except Exception as e:
            print(f"Error: {e}")


def main():
    """
    Main function - run all examples or choose one.
    """
    print("\n" + "#"*60)
    print("#  CHORD ALGORITHM - CUSTOM EXAMPLES")
    print("#"*60)
    
    print("\nSelect an example to run:")
    print("1. Simple Example")
    print("2. Test Join and Leave")
    print("3. Test Finger Tables")
    print("4. Stress Test")
    print("5. Interactive Mode")
    print("6. Run All (except interactive)")
    
    try:
        choice = input("\nEnter choice (1-6): ").strip()
        
        if choice == "1":
            simple_example()
        elif choice == "2":
            test_join_and_leave()
        elif choice == "3":
            test_finger_tables()
        elif choice == "4":
            stress_test()
        elif choice == "5":
            interactive_mode()
        elif choice == "6":
            simple_example()
            input("\nPress Enter to continue...")
            test_join_and_leave()
            input("\nPress Enter to continue...")
            test_finger_tables()
            input("\nPress Enter to continue...")
            stress_test()
        else:
            print("Invalid choice!")
            return
        
        print("\n" + "="*60)
        print("EXAMPLE COMPLETE")
        print("="*60)
    
    except KeyboardInterrupt:
        print("\n\nInterrupted by user.")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
