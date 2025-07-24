# market_participants.py

import hashlib
import numpy as np
from cryptography_lib import generate_keys, sign, generate_zkp_of_signature

class VerifiableSeller:
    """
    Represents a data seller with a cryptographic identity.
    Each seller can sign their data to prove ownership.
    """
    def __init__(self, seller_id):
        self.id = seller_id
        self.private_key, self.public_key = generate_keys()
        self.data = None
        print(f"  Created Seller '{self.id}' with public key {self.public_key.to_string().hex()[:10]}...")

    def set_data(self, data_stream):
        """Assigns a data stream to the seller."""
        self.data = data_stream

    def get_data_registration_package(self):
        """
        Creates a package containing the data, its hash, public key, and a ZKP.
        This package is submitted to the market for verification.
        """
        if self.data is None:
            raise ValueError("Seller data has not been set.")
            
        # Use a deterministic hash of the numpy array's byte representation
        data_hash = hashlib.sha256(self.data.tobytes()).digest()
        
        # Sign the hash to prove ownership
        signature = sign(self.private_key, data_hash)
        
        # Generate a ZKP to prove knowledge of the private key without revealing it
        zkp = generate_zkp_of_signature(data_hash, signature, self.public_key)
        
        return {
            "seller_id": self.id,
            "data": self.data,
            "data_hash": data_hash,
            "public_key": self.public_key,
            "zkp": zkp
        }

class BuyerWithCredentials:
    """
    Represents a data buyer who may hold Verifiable Credentials (VCs).
    """
    def __init__(self, buyer_id, true_valuation):
        self.id = buyer_id
        self.mu_n = true_valuation
        # A simple dictionary to act as a digital wallet for VCs
        self.wallet = {}
        print(f"  Created Buyer '{self.id}'.")

    def add_credential(self, credential_type, credential_object):
        """Adds a credential to the buyer's wallet."""
        self.wallet[credential_type] = credential_object
        print(f"    Buyer '{self.id}' received credential of type '{credential_type}'.")
        
    def present_credential(self, credential_type):
        """Presents a credential of a specific type if available."""
        return self.wallet.get(credential_type)