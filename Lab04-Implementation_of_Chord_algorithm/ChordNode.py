import hashlib
import random


class ChordNode:
    """
    Implementation of a Chord protocol node.
    Each node maintains a finger table and handles key-value storage.
    """
    
    def __init__(self, node_id, m=8):
        """
        Initialize a Chord node.
        
        Args:
            node_id: Unique identifier for the node
            m: Number of bits in the identifier space (default 8, supports 0-255)
        """
        self.id = node_id
        self.m = m
        self.max_nodes = 2 ** m
        
        # Successor and predecessor pointers
        self.successor = self
        self.predecessor = None
        
        # Finger table: stores m entries
        self.finger_table = [None] * m
        
        # Data storage (key-value pairs this node is responsible for)
        self.data = {}
        
        print(f"[Node {self.id}] Created")
    
    def __str__(self):
        return f"Node {self.id}"
    
    def __repr__(self):
        return f"ChordNode({self.id})"
    
    # ==================== HELPER FUNCTIONS ====================
    
    def in_range(self, key, start, end, inclusive_start=False, inclusive_end=False):
        """
        Check if key is in the range (start, end) on the Chord ring.
        Handles wrap-around cases.
        """
        if start == end:
            return inclusive_start or inclusive_end
        
        if start < end:
            if inclusive_start and inclusive_end:
                return start <= key <= end
            elif inclusive_start:
                return start <= key < end
            elif inclusive_end:
                return start < key <= end
            else:
                return start < key < end
        else:  # Wrap-around case
            if inclusive_start and inclusive_end:
                return key >= start or key <= end
            elif inclusive_start:
                return key >= start or key < end
            elif inclusive_end:
                return key > start or key <= end
            else:
                return key > start or key < end
    
    def distance(self, from_id, to_id):
        """Calculate clockwise distance on the ring"""
        if to_id >= from_id:
            return to_id - from_id
        else:
            return self.max_nodes - from_id + to_id
    
    # ==================== FINGER TABLE ====================
    
    def init_finger_table(self, existing_node):
        """
        Initialize finger table using an existing node in the network.
        This is called during the JOIN process.
        """
        # finger[0] = successor
        self.finger_table[0] = existing_node.find_successor((self.id + 1) % self.max_nodes)
        self.successor = self.finger_table[0]
        
        # Get predecessor from successor
        self.predecessor = self.successor.predecessor
        self.successor.predecessor = self
        
        # Initialize rest of finger table
        for i in range(self.m - 1):
            finger_start = (self.id + 2 ** (i + 1)) % self.max_nodes
            
            # If finger_start is in range [n, finger[i]], finger[i+1] = finger[i]
            if self.in_range(finger_start, self.id, self.finger_table[i].id, 
                           inclusive_start=True, inclusive_end=False):
                self.finger_table[i + 1] = self.finger_table[i]
            else:
                self.finger_table[i + 1] = existing_node.find_successor(finger_start)
        
        print(f"[Node {self.id}] Finger table initialized")
    
    def update_finger_table(self, s, i):
        """
        Update the finger table when a new node joins.
        s: the node that might be the i-th finger
        i: finger table index
        """
        finger_start = (self.id + 2 ** i) % self.max_nodes
        
        # If s is in the range [n, finger[i])
        if self.in_range(s.id, self.id, self.finger_table[i].id, 
                        inclusive_start=True, inclusive_end=False):
            self.finger_table[i] = s
            p = self.predecessor
            if p and p != self:
                p.update_finger_table(s, i)
    
    def fix_fingers(self):
        """
        Periodically called to update finger table entries.
        Part of the stabilization protocol.
        """
        for i in range(self.m):
            finger_start = (self.id + 2 ** i) % self.max_nodes
            self.finger_table[i] = self.find_successor(finger_start)
    
    # ==================== LOOKUP ====================
    
    def find_successor(self, key):
        """
        Find the successor node responsible for the given key.
        This is the core lookup operation in Chord.
        """
        # If key is between this node and its successor
        if self.in_range(key, self.id, self.successor.id, 
                        inclusive_end=True):
            return self.successor
        else:
            # Forward the query to the closest preceding node
            node = self.closest_preceding_node(key)
            if node == self:
                return self.successor
            return node.find_successor(key)
    
    def closest_preceding_node(self, key):
        """
        Find the closest node that precedes the key in the finger table.
        """
        # Search finger table from end to beginning
        for i in range(self.m - 1, -1, -1):
            if self.finger_table[i] and self.in_range(
                self.finger_table[i].id, self.id, key,
                inclusive_start=False, inclusive_end=False
            ):
                return self.finger_table[i]
        return self
    
    # ==================== JOIN FUNCTION ====================
    
    def join(self, existing_node=None):
        """
        Join the Chord network.
        
        Args:
            existing_node: A node already in the network (None if first node)
        """
        if existing_node:
            print(f"[Node {self.id}] Joining network through Node {existing_node.id}")
            
            # Initialize finger table using existing node
            self.init_finger_table(existing_node)
            
            # Update other nodes' finger tables
            self.update_others()
            
            # Transfer keys from successor
            self.transfer_keys()
            
            print(f"[Node {self.id}] Successfully joined the network")
        else:
            # First node in the network
            print(f"[Node {self.id}] Creating new Chord network")
            for i in range(self.m):
                self.finger_table[i] = self
            self.predecessor = self
            self.successor = self
    
    def update_others(self):
        """
        Update finger tables of existing nodes after joining.
        """
        for i in range(self.m):
            # Find last node p whose i-th finger might be this node
            p_id = (self.id - 2 ** i) % self.max_nodes
            p = self.find_predecessor(p_id)
            if p and p != self:
                p.update_finger_table(self, i)
    
    def find_predecessor(self, key):
        """Find the predecessor of a given key"""
        node = self
        while not self.in_range(key, node.id, node.successor.id, 
                               inclusive_end=True):
            node = node.closest_preceding_node(key)
            if node == self:
                break
        return node
    
    # ==================== STABILIZATION FUNCTIONS ====================
    
    def stabilize(self):
        """
        Periodically called to verify and update successor and predecessor.
        Ensures the Chord ring remains consistent.
        """
        # Ask successor for its predecessor
        x = self.successor.predecessor
        
        # If successor's predecessor is between this node and successor,
        # it should be our new successor
        if x and x != self and self.in_range(
            x.id, self.id, self.successor.id,
            inclusive_start=False, inclusive_end=False
        ):
            self.successor = x
            self.finger_table[0] = x
        
        # Notify successor that this node might be its predecessor
        self.successor.notify(self)
    
    def notify(self, node):
        """
        Called by another node thinking it might be our predecessor.
        """
        if self.predecessor is None or self.in_range(
            node.id, self.predecessor.id, self.id,
            inclusive_start=False, inclusive_end=False
        ):
            self.predecessor = node
    
    def check_predecessor(self):
        """
        Check if predecessor has failed.
        In simulation, we just check if it's None.
        """
        if self.predecessor and not self.is_alive(self.predecessor):
            print(f"[Node {self.id}] Predecessor {self.predecessor.id} failed")
            self.predecessor = None
    
    def is_alive(self, node):
        """
        Check if a node is alive.
        In real implementation, this would ping the node.
        """
        return node is not None
    
    # ==================== NODE DEPARTURE ====================
    
    def leave(self):
        """
        Gracefully leave the Chord network.
        Transfer keys to successor and update pointers.
        """
        print(f"[Node {self.id}] Leaving the network")
        
        # Transfer all keys to successor
        if self.successor and self.successor != self:
            print(f"[Node {self.id}] Transferring {len(self.data)} keys to Node {self.successor.id}")
            for key, value in self.data.items():
                self.successor.data[key] = value
            self.data.clear()
        
        # Update predecessor's successor
        if self.predecessor and self.predecessor != self:
            self.predecessor.successor = self.successor
            if self.predecessor.finger_table:
                self.predecessor.finger_table[0] = self.successor
        
        # Update successor's predecessor
        if self.successor and self.successor != self:
            self.successor.predecessor = self.predecessor
        
        print(f"[Node {self.id}] Left the network")
    
    # ==================== DATA OPERATIONS ====================
    
    def put(self, key, value):
        """
        Store a key-value pair in the appropriate node.
        """
        key_hash = self.hash_key(key)
        responsible_node = self.find_successor(key_hash)
        responsible_node.data[key] = value
        print(f"[Node {self.id}] PUT '{key}' -> '{value}' (hash={key_hash}, stored at Node {responsible_node.id})")
        return responsible_node
    
    def get(self, key):
        """
        Retrieve a value for the given key.
        """
        key_hash = self.hash_key(key)
        responsible_node = self.find_successor(key_hash)
        value = responsible_node.data.get(key, None)
        print(f"[Node {self.id}] GET '{key}' (hash={key_hash}, from Node {responsible_node.id}) = {value}")
        return value
    
    def hash_key(self, key):
        """
        Hash a key to an integer in the range [0, 2^m - 1].
        """
        hash_obj = hashlib.sha1(str(key).encode())
        hash_int = int(hash_obj.hexdigest(), 16)
        return hash_int % self.max_nodes
    
    def transfer_keys(self):
        """
        Transfer appropriate keys from successor when joining.
        """
        if not self.successor or self.successor == self:
            return
        
        keys_to_transfer = []
        for key in list(self.successor.data.keys()):
            key_hash = self.hash_key(key)
            # If key should be stored at this node
            if self.in_range(key_hash, self.predecessor.id if self.predecessor else self.id, 
                           self.id, inclusive_end=True):
                keys_to_transfer.append(key)
        
        for key in keys_to_transfer:
            self.data[key] = self.successor.data.pop(key)
        
        if keys_to_transfer:
            print(f"[Node {self.id}] Transferred {len(keys_to_transfer)} keys from Node {self.successor.id}")
    
    # ==================== DISPLAY FUNCTIONS ====================
    
    def print_info(self):
        """Print detailed information about this node"""
        print(f"\n{'='*50}")
        print(f"Node {self.id} Information:")
        print(f"{'='*50}")
        print(f"Predecessor: {self.predecessor.id if self.predecessor else 'None'}")
        print(f"Successor: {self.successor.id if self.successor else 'None'}")
        print(f"\nFinger Table:")
        for i in range(self.m):
            start = (self.id + 2 ** i) % self.max_nodes
            if self.finger_table[i]:
                print(f"  finger[{i}]: start={start:3d}, node={self.finger_table[i].id:3d}")
        print(f"\nStored Keys: {len(self.data)}")
        if self.data:
            for key, value in self.data.items():
                print(f"  '{key}' (hash={self.hash_key(key)}) = '{value}'")
        print(f"{'='*50}\n")
