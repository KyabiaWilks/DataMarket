import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error

# 导入自定义模块
from market_participants import VerifiableSeller, BuyerWithCredentials
from market_mechanisms import Marketplace, HonestAuction, UCBPricer, RevenueDivider


def generate_data(M=10, T=100):
    # """Generates simulated seller features (X) and a buyer's task (Y)."""
    """
    生成模拟的卖家特征 (X) 和买家的任务 (Y)。
    Args:
        M (int): 卖家数量
        T (int): 特征长度
    Returns:
        tuple: 包含特征矩阵 X (M, T) 和目标向量 Y (T,) 的元组
    """
    X = np.random.rand(M, T) * 10
    true_weights = np.random.randn(M)
    Y = np.dot(true_weights, X) + np.random.normal(0, 0.5, T)
    return X, Y


def gain_function_rmse(y_true, y_pred):
    """
    计算 1：Normalized RMSE 作为增益函数
    Args:
        y_true (np.array): 真实目标值
        y_pred (np.array): 预测值
    Returns:
        float: 预测增益 G
    """
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    y_std = np.std(y_true)
    if y_std == 0:
        return 1.0
    normalized_rmse = rmse / y_std
    return max(0, 1 - normalized_rmse)


# --- Main Simulation Logic ---

if __name__ == "__main__":
    NUM_SELLERS = 5

    # =========================================================================
    # 阶段 1: 设置和数据注册，使用加密验证
    # =========================================================================
    print("--- PHASE 1: Market Setup and Seller Data Registration ---")

    # 1. 初始化市场和验证服务
    marketplace = Marketplace()

    # 创建卖家并生成他们的数据
    sellers = [VerifiableSeller(f"Seller-{i+1}") for i in range(NUM_SELLERS)]

    for seller in sellers:
        seller_data, _ = generate_data(M=1, T=100)
        seller.set_data(seller_data)

    # 创建一个恶意卖家，试图提交重复数据
    malicious_seller = VerifiableSeller("MaliciousSeller")
    malicious_seller.set_data(sellers[0].data)  # Copy data from Seller-1
    sellers.append(malicious_seller)

    # 3. 卖家生成数据并尝试注册
    registered_features = []
    seller_identities = []  # Keep track of who owns which registered feature

    print("\n[Market] Opening data registration...")
    for seller in sellers:
        # 为了模拟 ，非恶意卖家生成随机数据
        if seller.id != "MaliciousSeller":
            seller_data, _ = generate_data(M=1, T=100)
            seller.set_data(seller_data)  # seller_data is (1, T), we need (T,)

        # 卖家创建包含数据、签名和零知识证明的注册包
        package = seller.get_data_registration_package()

        # 市场验证卖家的数据包
        if marketplace.verification_service.register_data(package):
            registered_features.append(package["data"])
            seller_identities.append(seller.id)

    # 4. 确认注册的数据
    if not registered_features:
        print("\nNo valid data was registered. Terminating simulation.")
        exit()

    X_verified = np.array(registered_features)
    print(f"\n[Market] Data registration closed. {X_verified.shape} features verified.")
    print(f"Verified data providers: {seller_identities}")

    # =========================================================================
    # 阶段 2: 使用可验证凭证的拍卖模拟
    # =========================================================================
    print("\n\n--- PHASE 2: Auction Simulation with Buyer Credentials ---")

    # 1. 使用验证过的数据初始化经济机制
    ml_model = LinearRegression()
    price_range = (50, 500)
    pricer = UCBPricer(price_range=price_range, num_experts=20, confidence_c=2.0)
    auction = HonestAuction(ml_model=ml_model, gain_function=gain_function_rmse)
    divider = RevenueDivider(ml_model=ml_model, gain_function=gain_function_rmse)

    # 2. 生成买家的预测任务
    _, Y_task = generate_data(M=X_verified.shape[0], T=100)

    # 3. 定义一个需要特定凭证的任务
    REQUIRED_CREDENTIAL = "Certified_Medical_Researcher"
    print(
        f"\n[Market] A new prediction task is available. Access requires '{REQUIRED_CREDENTIAL}' credential."
    )

    # 4. 创建两个买家：一个有凭证，一个没有
    buyer_qualified = BuyerWithCredentials("Dr. Alice", 250.0)
    # 一个可信的 "Issuer" 给 Dr. Alice 一个有效的凭证
    valid_vc = {
        "issuer": "TrustedMedicalBoard",
        "type": REQUIRED_CREDENTIAL,
        "status": "valid",
    }
    buyer_qualified.add_credential(REQUIRED_CREDENTIAL, valid_vc)

    buyer_unqualified = BuyerWithCredentials("Bob", 300.0)

    # 5. 模拟每个买家的交易
    for buyer in [buyer_qualified, buyer_unqualified]:
        print(f"\n--- Simulating transaction for {buyer.id} ---")

        # 步骤 3.5: 验证买家的凭证
        if not marketplace.verify_buyer_credentials(buyer, REQUIRED_CREDENTIAL):
            continue  # If verification fails, the transaction stops here.

        # 如果验证通过，继续拍卖流程
        # 步骤 1: 市场设定价格
        p_n, chosen_index = pricer.choose_price()
        print(f"Step 1: Market offers price p_n = {p_n:.2f}")

        # 步骤 2 & 3: 买家到达并出价
        b_n = buyer.mu_n
        print(f"Step 2&3: Buyer '{buyer.id}' bids b_n = {b_n:.2f}")

        # 步骤 4 & 5: 市场分配数据并计算预测增益
        gain_actual = auction.get_prediction_gain(X_verified, Y_task, p_n, b_n)
        print(f"Step 4&5: Achieved prediction gain: {gain_actual:.4f}")

        # 步骤 6: 市场收取收益
        revenue_n = auction.calculate_revenue(X_verified, Y_task, p_n, b_n)
        print(f"Step 6: Market collects revenue r_n = {revenue_n:.2f}")

        # 步骤 7: Pricer 更新其统计信息
        pricer.update_stats(chosen_index, revenue_n)
        print("Step 7: Pricing model updated.")

        # 步骤 8: 市场将收益分配给验证过的卖家
        shapley_values = divider.shapley_robust(X_verified, Y_task, K=50)
        if np.sum(shapley_values) > 0:
            allocation_ratios = shapley_values / np.sum(shapley_values)
        else:
            allocation_ratios = np.ones(X_verified.shape) / X_verified.shape

        seller_revenues = revenue_n * allocation_ratios

        print("Step 8: Revenue divided among sellers:")
        for i, seller_id in enumerate(seller_identities):
            print(f"  - {seller_id}: ${seller_revenues[i]:.2f}")
