from cryptography_lib import verify_zkp

class MarketVerificationService:
    def __init__(self):
        # 维护一个已注册数据哈希的集合，防止重复提交
        self.registered_data_hashes = set()

    def register_data(self, seller, data, data_hash, public_key, zkp):
        """
        注册并验证一个卖家的数据。
        """
        # 1. 检查数据是否已经被注册 (防止直接复制)
        if data_hash in self.registered_data_hashes:
            print(f"拒绝注册：数据 {data_hash[:10]}... 已存在。")
            return False
            
        # 2. 验证ZKP (防止伪造所有权)
        # 验证器只知道公钥、数据哈希和证明本身
        if not verify_zkp(public_key, data_hash, zkp):
            print(f"拒绝注册：卖家 {seller.id} 的ZKP验证失败。")
            return False
            
        # 3. 注册成功
        self.registered_data_hashes.add(data_hash)
        print(f"卖家 {seller.id} 的数据 {data_hash[:10]}... 验证通过并成功注册。")
        return True