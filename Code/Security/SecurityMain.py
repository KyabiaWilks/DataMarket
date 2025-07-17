def dataRegister():
    verification_service = MarketVerificationService()
    # sellers =
    # registered_features =
    for seller in sellers:
        # 生成模拟数据并分配给卖家
        seller_data, _ = generate_data(M=1, T=100) 
        seller.set_data(seller_data)
        
        # 卖家生成签名和证明
        data, data_hash, pk, zkp = seller.get_data_signature_and_proof()
        
        # 市场进行验证和注册
        if verification_service.register_data(seller, data, data_hash, pk, zkp):
            registered_features.append(data)

        return registered_features
    
def qualifySet():
    # --- 模拟单个买家 n 的交易 ---
    print("--- 开始模拟单次交易 (带凭证验证) ---")

    # 假设一个需要特定凭证才能访问的数据任务
    REQUIRED_CREDENTIAL = "Certified_Medical_Researcher"

    # 创建一个有凭证的买家和一个没有凭证的买家
    buyer_qualified = BuyerWithCredentials("QualifiedBuyer", 250.0)
    # 假设一个可信的“发行方”为该买家颁发了凭证
    buyer_qualified.add_credential(REQUIRED_CREDENTIAL, "A_VALID_VC_OBJECT")

    buyer_unqualified = BuyerWithCredentials("UnqualifiedBuyer", 300.0)

    # --- 场景1：合格的买家 ---
    buyer = buyer_qualified
    print(f"\n处理买家: {buyer.id}")

    # 步骤 1: 市场定价
    p_n, _ = pricer.choose_price()
    print(f"步骤 1: 市场设定价格 p_n = {p_n:.2f}")

    # 步骤 2 & 3: 买家到达并出价
    b_n = buyer.mu_n
    print(f"步骤 2 & 3: 买家出价 b_n = {b_n:.2f}")

    # 新增步骤 3.5: 凭证验证
    print(f"步骤 3.5: 市场验证所需凭证 '{REQUIRED_CREDENTIAL}'...")
    if marketplace.verify_credentials(buyer, REQUIRED_CREDENTIAL):
        #... 如果验证通过，则继续执行步骤 4-8...
        print("  凭证有效，继续交易。")
        #... (gain_actual =..., revenue_n =..., etc.)
    else:
        print("  凭证无效，交易终止。")

    # --- 场景2：不合格的买家 ---
    buyer = buyer_unqualified
    print(f"\n处理买家: {buyer.id}")
    #... (重复上述流程，但这次验证会失败)