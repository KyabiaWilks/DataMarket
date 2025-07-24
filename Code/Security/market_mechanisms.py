# market_mechanisms.py

import numpy as np
from scipy.integrate import quad
from sklearn.metrics.pairwise import cosine_similarity
from cryptography_lib import verify_zkp

# --- New Security-Focused Mechanisms ---

class MarketVerificationService:
    """
    A service within the marketplace responsible for verifying and registering
    seller data to ensure originality and prevent simple duplication.
    """
    def __init__(self):
        # A set to store the hashes of all data ever registered in the market.
        self.registered_data_hashes = set()

    def register_data(self, registration_package):
        """
        Verifies a seller's data package and registers it if valid.

        Args:
            registration_package (dict): The package from a VerifiableSeller.

        Returns:
            bool: True if registration is successful, False otherwise.
        """
        data_hash = registration_package["data_hash"]
        public_key = registration_package["public_key"]
        zkp = registration_package["zkp"]

        # Check 1: Uniqueness. Has this exact data been submitted before?
        if data_hash in self.registered_data_hashes:
            print(f"  [Verification] FAILED: Data with hash {data_hash.hex()[:10]}... already exists. Rejecting.")
            return False
            
        # Check 2: Ownership Proof. Does the seller provably own this data?
        # This simulates verifying the ZKP.
        if not verify_zkp(public_key, data_hash, zkp):
            print(f"  [Verification] FAILED: ZKP for data hash {data_hash.hex()[:10]}... is invalid. Rejecting.")
            return False
            
        # If all checks pass, register the data
        self.registered_data_hashes.add(data_hash)
        print(f"  [Verification] SUCCESS: Data from seller '{registration_package['seller_id']}' verified and registered.")
        return True

class Marketplace:
    """
    A central marketplace entity that can enforce rules, such as requiring
    Verifiable Credentials for certain tasks.
    """
    def __init__(self):
        self.verification_service = MarketVerificationService()

    def verify_buyer_credentials(self, buyer, required_credential_type):
        """
        Checks if a buyer holds the necessary credential for a task.
        """
        if required_credential_type is None:
            return True # This task is public and requires no credentials.
            
        credential = buyer.present_credential(required_credential_type)
        
        # In a real system, this would involve a cryptographic verification of the VC's signature.
        if credential and self._is_credential_valid(credential):
            print(f"  [Marketplace] Buyer '{buyer.id}' presented a valid '{required_credential_type}' credential. Access granted.")
            return True
        else:
            print(f"  [Marketplace] Buyer '{buyer.id}' failed credential check for '{required_credential_type}'. Access denied.")
            return False

    def _is_credential_valid(self, credential):
        # MOCK: A real implementation would check the issuer's signature,
        # check against a revocation list, etc.
        return credential.get("status") == "valid"


# --- Original Economic Mechanisms (from previous steps) ---

class HonestAuction:
    def __init__(self, ml_model, gain_function):
        self.ml_model = ml_model
        self.gain_function = gain_function

    def _allocation_function(self, X, p_n, b_n, noise_std=0.1):
        if b_n >= p_n:
            return X
        else:
            noise_magnitude = max(0, p_n - b_n)
            noise = np.random.normal(0, noise_std * noise_magnitude, X.shape)
            return X + noise

    def get_prediction_gain(self, X, Y, p_n, b_n):
        X_tilde = self._allocation_function(X, p_n, b_n)
        X_train = X_tilde.T
        y_train = Y
        self.ml_model.fit(X_train, y_train)
        y_pred = self.ml_model.predict(X_train)
        return self.gain_function(y_train, y_pred)

    def calculate_revenue(self, X, Y, p_n, b_n):
        gain_at_b_n = self.get_prediction_gain(X, Y, p_n, b_n)
        def gain_as_function_of_bid(z):
            return self.get_prediction_gain(X, Y, p_n, z)
        integral_part, _ = quad(gain_as_function_of_bid, 0, b_n)
        revenue = b_n * gain_at_b_n - integral_part
        return max(0, revenue)

class UCBPricer:
    def __init__(self, price_range, num_experts, confidence_c=2.0):
        self.experts = np.linspace(price_range, price_range[1], num_experts)
        self.num_experts = num_experts
        self.c = confidence_c
        self.counts = np.zeros(num_experts)
        self.values = np.zeros(num_experts)
        self.total_rounds = 0

    def choose_price(self):
        self.total_rounds += 1
        for i in range(self.num_experts):
            if self.counts[i] == 0:
                return self.experts[i], i
        ucb_values = self.values + np.sqrt((self.c * np.log(self.total_rounds)) / self.counts)
        chosen_expert_index = np.argmax(ucb_values)
        return self.experts[chosen_expert_index], chosen_expert_index

    def update_stats(self, chosen_expert_index, reward):
        self.counts[chosen_expert_index] += 1
        n = self.counts[chosen_expert_index]
        old_value = self.values[chosen_expert_index]
        new_value = ((n - 1) / n) * old_value + (1 / n) * reward
        self.values[chosen_expert_index] = new_value

class RevenueDivider:
    def __init__(self, ml_model, gain_function):
        self.ml_model = ml_model
        self.gain_function = gain_function

    def _get_gain_for_subset(self, X_subset, Y):
        if X_subset.shape == 0:
            return 0.0
        X_train = X_subset.T
        y_train = Y
        self.ml_model.fit(X_train, y_train)
        y_pred = self.ml_model.predict(X_train)
        return self.gain_function(y_train, y_pred)

    def shapley_approx(self, X, Y, K):
        M, T = X.shape
        shapley_values = np.zeros(M)
        for _ in range(K):
            permutation = np.random.permutation(M)
            gain_predecessors = 0.0
            for i in range(M):
                feature_idx = permutation[i]
                predecessor_indices = permutation[:i]
                current_subset_indices = np.append(predecessor_indices, feature_idx)
                gain_current = self._get_gain_for_subset(X[current_subset_indices], Y)
                marginal_contribution = gain_current - gain_predecessors
                shapley_values[feature_idx] += marginal_contribution
                gain_predecessors = gain_current
        return shapley_values / K

    def shapley_robust(self, X, Y, K, lambda_param=np.log(2)):
        approx_shapley = self.shapley_approx(X, Y, K)
        M = X.shape
        robust_shapley = np.zeros(M)
        similarity_matrix = cosine_similarity(X)
        for m in range(M):
            total_similarity = np.sum(similarity_matrix[m]) - 1
            penalty_factor = np.exp(-lambda_param * total_similarity)
            robust_shapley[m] = approx_shapley[m] * penalty_factor
        return robust_shapley