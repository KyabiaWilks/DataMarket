import numpy as np
from scipy.integrate import quad
from sklearn.metrics.pairwise import cosine_similarity
from cryptography_lib import verify_zkp

# ============================================================
# 新增的安全机制，确保数据的原创性和卖家的所有权
# ============================================================

class MarketVerificationService:
    """
    市场验证服务，负责验证和注册卖家数据，以确保原创性并防止简单复制
    """

    def __init__(self):
        # 用于存储所有已注册数据的哈希值的集合，以确保数据的唯一性
        self.registered_data_hashes = set()

    def register_data(self, registration_package):
        """
        验证卖家提交的数据包，确保数据的唯一性和所有权
        Args:
            registration_package (dict): 包含卖家ID、数据、数据哈希、公钥和零知识证明的注册包
        Returns:
            bool: 如果数据验证成功并注册，则返回 True，否则返回 False
        """
        data_hash = registration_package["data_hash"]
        public_key = registration_package["public_key"]
        zkp = registration_package["zkp"]

        # 检查数据哈希是否已存在于注册集中
        if data_hash in self.registered_data_hashes:
            print(
                f"  [Verification] FAILED: Data with hash {data_hash.hex()[:10]}... already exists. Rejecting."
            )
            return False

        # 检查卖家是否拥有数据的所有权，模拟验证零知识证明（ZKP）
        if not verify_zkp(public_key, data_hash, zkp):
            print(
                f"  [Verification] FAILED: ZKP for data hash {data_hash.hex()[:10]}... is invalid. Rejecting."
            )
            return False

        # 如果验证通过，注册数据哈希
        self.registered_data_hashes.add(data_hash)
        print(
            f"  [Verification] SUCCESS: Data from seller '{registration_package['seller_id']}' verified and registered."
        )
        return True


class Marketplace:
    """中央市场实体，可以执行规则，例如针对某些任务的可验证凭证"""

    def __init__(self):
        self.verification_service = MarketVerificationService()

    def verify_buyer_credentials(self, buyer, required_credential_type):
        """检查买家是否持有必要的凭证
        Args:
            buyer (BuyerWithCredentials): 买家对象
            required_credential_type (str): 需要的凭证类型
        Returns:
            bool: 如果买家持有所需凭证，则返回 True，否则返回 False
        """
        if required_credential_type is None:
            return True  # 这个任务是公开的，不需要凭证

        credential = buyer.present_credential(required_credential_type)

        # 在一个真实系统中，这将涉及对VC签名的加密验证，这里我们通过检查一个简单的状态字段来模拟这一点
        if credential and self._is_credential_valid(credential):
            print(
                f"  [Marketplace] Buyer '{buyer.id}' presented a valid '{required_credential_type}' credential. Access granted."
            )
            return True
        else:
            print(
                f"  [Marketplace] Buyer '{buyer.id}' failed credential check for '{required_credential_type}'. Access denied."
            )
            return False

    def _is_credential_valid(self, credential):
        """检查凭证是否有效"""
        return credential.get("status") == "valid"


class HonestAuction:
    """一种密封竞标拍卖机制，买家在不知道其他买家出价的情况下提交出价"""

    def __init__(self, ml_model, gain_function):
        self.ml_model = ml_model
        self.gain_function = gain_function

    def _allocation_function(self, X, p_n, b_n, noise_std=0.1):
        """分配函数 AF* (Allocation Function)
        根据价格 p_n 和出价 b_n 的差异，向数据 X 添加高斯噪声来降级其质量
        Args:
            X (np.array): 原始特征数据 (M, T)
            p_n (float): 市场设定的价格
            b_n (float): 买家的出价
            noise_std (float): 基础噪声的标准差
        Returns:
            np.array: 降级后的数据 X_tilde
        """
        if b_n >= p_n:
            return X
        else:
            noise_magnitude = max(0, p_n - b_n)
            noise = np.random.normal(0, noise_std * noise_magnitude, X.shape)
            return X + noise

    def get_prediction_gain(self, X, Y, p_n, b_n):
        """
        在给定价格和出价下，计算预测增益 G
        Args:
            X (np.array): 原始特征数据 (M, T)
            Y (np.array): 目标预测任务数据 (T,)
            p_n (float): 市场价格
            b_n (float): 买家出价
        Returns:
            float: 预测增益 G
        """
        X_tilde = self._allocation_function(X, p_n, b_n)
        if X_tilde is None:
            raise ValueError("_allocation_function returned None")

        # print(f"X_tilde.shape before squeeze: {X_tilde.shape}")

        if X_tilde.ndim == 3:
            X_tilde = X_tilde.squeeze(axis=1)
            # print(f"X_tilde.shape after squeeze: {X_tilde.shape}")

        X_train = X_tilde.T  # 一定要先赋值，后续才可访问

        # print(f"X_train.shape before fit: {X_train.shape}")
        # print(f"y_train.shape: {Y.shape}")

        self.ml_model.fit(X_train, Y)
        y_pred = self.ml_model.predict(X_train)
        return self.gain_function(Y, y_pred)

    def calculate_revenue(self, X, Y, p_n, b_n):
        """
        计算市场从买家收取的收益
        Args:
            X (np.array): 原始特征数据 (M, T)
            Y (np.array): 目标预测任务数据 (T,)
            p_n (float): 市场价格
            b_n (float): 买家出价
        Returns:
            float: 市场从买家收取的收益
        """
        gain_at_b_n = self.get_prediction_gain(X, Y, p_n, b_n)

        def gain_as_function_of_bid(z):
            return self.get_prediction_gain(X, Y, p_n, z)

        integral_part, _ = quad(gain_as_function_of_bid, 0, b_n)
        revenue = b_n * gain_at_b_n - integral_part
        return max(0, revenue)


class UCBPricer:
    """基于UCB (Upper Confidence Bound) 算法的定价器，用于动态定价市场价格"""

    def __init__(self, price_range, num_experts, confidence_c=2.0):
        self.experts = np.linspace(price_range[0], price_range[1], num_experts)
        self.num_experts = num_experts
        self.c = confidence_c
        self.counts = np.zeros(num_experts)
        self.values = np.zeros(num_experts)
        self.total_rounds = 0

    def choose_price(self):
        """根据UCB规则选择一个价格"""
        self.total_rounds += 1
        for i in range(self.num_experts):
            if self.counts[i] == 0:
                return self.experts[i], i
        ucb_values = self.values + np.sqrt(
            (self.c * np.log(self.total_rounds)) / self.counts
        )
        chosen_expert_index = np.argmax(ucb_values)
        return float(self.experts[chosen_expert_index]), chosen_expert_index

    def update_stats(self, chosen_expert_index, reward):
        """在一次交易后，更新被选中专家的统计数据"""
        self.counts[chosen_expert_index] += 1
        n = self.counts[chosen_expert_index]
        old_value = self.values[chosen_expert_index]
        new_value = ((n - 1) / n) * old_value + (1 / n) * reward
        self.values[chosen_expert_index] = new_value


class RevenueDivider:
    """一个简单的收益分配器，使用鲁棒的Shapley值分配收益给卖家"""

    def __init__(self, ml_model, gain_function):
        self.ml_model = ml_model
        self.gain_function = gain_function

    def _get_gain_for_subset(self, X_subset, Y):
        """计算给定特征子集的增益
        Args:
            X_subset (np.array): 特征子集 (M', T)
            Y (np.array): 目标预测任务数据 (T,)
        Returns:
            float: 特征子集的预测增益
        """
        if X_subset.shape == 0:
            return 0.0
        X_train = X_subset.T
        y_train = Y

        # print(f"2X_train.shape: {X_train.shape}")
        # print(f"2y_train.shape: {y_train.shape}")

        self.ml_model.fit(X_train, y_train)
        y_pred = self.ml_model.predict(X_train)
        return self.gain_function(y_train, y_pred)

    def shapley_approx(self, X, Y, K):
        """近似Shapley值 (Algorithm 2: SHAPLEY-APPROX).
        Args:
            X (np.array): 所有卖家的特征数据 (M, T)
            Y (np.array): 目标预测任务数据 (T,)
            K (int): 蒙特卡洛采样的迭代次数
        Returns:
            np.array: 每个卖家的近似Shapley值 (M,)
        """
        X = np.squeeze(X)
        if X.ndim != 2:
            raise ValueError(
                f"X must be 2-dimensional after squeeze, but got shape: {X.shape}"
            )

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
        """计算鲁棒的Shapley值 (Algorithm 3: SHAPLEY-ROBUST).
        Args:
            X (np.array): 所有卖家的特征数据 (M, T)
            Y (np.array): 目标预测任务数据 (T,)
            K (int): 蒙特卡洛采样的迭代次数
            lambda_param (float): 指数惩罚项的强度参数
        Returns:
            np.array: 每个卖家的鲁棒Shapley值 (M,)
        """
        X = np.squeeze(X)
        if X.ndim != 2:
            raise ValueError(
                f"[shapley_robust] X must be 2D after squeeze, got shape: {X.shape}"
            )

        approx_shapley = self.shapley_approx(X, Y, K)
        M, T = X.shape
        robust_shapley = np.zeros(M)
        similarity_matrix = cosine_similarity(X)
        for m in range(M):
            total_similarity = np.sum(similarity_matrix[m]) - 1
            penalty_factor = np.exp(-lambda_param * total_similarity)
            robust_shapley[m] = approx_shapley[m] * penalty_factor
        return robust_shapley
