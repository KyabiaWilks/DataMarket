# main.py

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# Import our custom modules
from market_participants import VerifiableSeller, BuyerWithCredentials
from market_mechanisms import Marketplace, HonestAuction, UCBPricer, RevenueDivider

# --- Simulation Setup ---

def generate_data(M=10, T=100):
    """Generates simulated seller features (X) and a buyer's task (Y)."""
    X = np.random.rand(M, T) * 10
    true_weights = np.random.randn(M)
    Y = np.dot(true_weights, X) + np.random.normal(0, 0.5, T)
    return X, Y

def gain_function_rmse(y_true, y_pred):
    """Calculates 1 - Normalized RMSE as the prediction gain function."""
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    y_std = np.std(y_true)
    if y_std == 0: return 1.0
    normalized_rmse = rmse / y_std
    return max(0, 1 - normalized_rmse)

# --- Main Simulation Logic ---

if __name__ == "__main__":
    NUM_SELLERS = 5
    
    # =========================================================================
    # PHASE 1: SETUP AND DATA REGISTRATION WITH CRYPTOGRAPHIC VERIFICATION
    # =========================================================================
    print("--- PHASE 1: Market Setup and Seller Data Registration ---")
    
    # 1. Initialize the marketplace and its verification service
    marketplace = Marketplace()
    
    # 2. Create sellers
    sellers = [VerifiableSeller(f"Seller-{i+1}") for i in range(NUM_SELLERS)]
    
    for seller in sellers:
        seller_data, _ = generate_data(M=1, T=100)
        seller.set_data(seller_data)

    # Add a malicious seller who tries to submit duplicate data
    malicious_seller = VerifiableSeller("MaliciousSeller")
    malicious_seller.set_data(sellers[0].data) # Copy data from Seller-1
    sellers.append(malicious_seller)

    # 3. Sellers generate data and attempt to register it
    registered_features = []
    seller_identities = []  # Keep track of who owns which registered feature

    print("\n[Market] Opening data registration...")
    for seller in sellers:
        # For simulation, generate random data for each non-malicious seller
        if seller.id!= "MaliciousSeller":
            seller_data, _ = generate_data(M=1, T=100)
            seller.set_data(seller_data) # seller_data is (1, T), we need (T,)
        
        # Seller creates their registration package with data, signature, and ZKP
        package = seller.get_data_registration_package()
        
        # Marketplace attempts to verify and register the data
        if marketplace.verification_service.register_data(package):
            registered_features.append(package["data"])
            seller_identities.append(seller.id)

    # 4. Finalize the market's verified dataset
    if not registered_features:
        print("\nNo valid data was registered. Terminating simulation.")
        exit()
        
    X_verified = np.array(registered_features)
    print(f"\n[Market] Data registration closed. {X_verified.shape} features verified.")
    print(f"Verified data providers: {seller_identities}")
    
    # =========================================================================
    # PHASE 2: AUCTION WITH VERIFIABLE CREDENTIALS
    # =========================================================================
    print("\n\n--- PHASE 2: Auction Simulation with Buyer Credentials ---")

    # 1. Initialize economic mechanisms with the verified data
    ml_model = LinearRegression()
    price_range = (50, 500)
    pricer = UCBPricer(price_range=price_range, num_experts=20, confidence_c=2.0)
    auction = HonestAuction(ml_model=ml_model, gain_function=gain_function_rmse)
    divider = RevenueDivider(ml_model=ml_model, gain_function=gain_function_rmse)

    # 2. Generate a buyer's prediction task
    _, Y_task = generate_data(M=X_verified.shape[0], T=100)

    # 3. Define a task that requires a specific credential
    REQUIRED_CREDENTIAL = "Certified_Medical_Researcher"
    print(f"\n[Market] A new prediction task is available. Access requires '{REQUIRED_CREDENTIAL}' credential.")

    # 4. Create two buyers: one qualified, one not
    buyer_qualified = BuyerWithCredentials("Dr. Alice", 250.0)
    # A trusted "Issuer" gives Dr. Alice a valid VC
    valid_vc = {"issuer": "TrustedMedicalBoard", "type": REQUIRED_CREDENTIAL, "status": "valid"}
    buyer_qualified.add_credential(REQUIRED_CREDENTIAL, valid_vc)

    buyer_unqualified = BuyerWithCredentials("Bob", 300.0)

    # 5. Simulate transaction for each buyer
    for buyer in [buyer_qualified, buyer_unqualified]:
        print(f"\n--- Simulating transaction for {buyer.id} ---")
        
        # Step 3.5: Credential Verification
        if not marketplace.verify_buyer_credentials(buyer, REQUIRED_CREDENTIAL):
            continue # If verification fails, the transaction stops here.

        # If verification passes, proceed with the auction
        # Step 1: Market sets a price
        p_n, chosen_index = pricer.choose_price()
        print(f"Step 1: Market offers price p_n = {p_n:.2f}")

        # Step 2 & 3: Buyer makes an honest bid
        b_n = buyer.mu_n
        print(f"Step 2&3: Buyer '{buyer.id}' bids b_n = {b_n:.2f}")

        # Step 4 & 5: Market allocates data and buyer gets prediction gain
        gain_actual = auction.get_prediction_gain(X_verified, Y_task, p_n, b_n)
        print(f"Step 4&5: Achieved prediction gain: {gain_actual:.4f}")

        # Step 6: Market collects revenue
        revenue_n = auction.calculate_revenue(X_verified, Y_task, p_n, b_n)
        print(f"Step 6: Market collects revenue r_n = {revenue_n:.2f}")

        # Step 7: Pricer updates its statistics
        pricer.update_stats(chosen_index, revenue_n)
        print("Step 7: Pricing model updated.")

        # Step 8: Market divides revenue among the verified sellers
        shapley_values = divider.shapley_robust(X_verified, Y_task, K=50)
        if np.sum(shapley_values) > 0:
            allocation_ratios = shapley_values / np.sum(shapley_values)
        else:
            allocation_ratios = np.ones(X_verified.shape) / X_verified.shape
        
        seller_revenues = revenue_n * allocation_ratios
        
        print("Step 8: Revenue divided among sellers:")
        for i, seller_id in enumerate(seller_identities):
            print(f"  - {seller_id}: ${seller_revenues[i]:.2f}")