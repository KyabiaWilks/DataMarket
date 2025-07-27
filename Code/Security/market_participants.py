import hashlib
import numpy as np
from cryptography_lib import generate_keys, sign, generate_zkp_of_signature

class VerifiableSeller:
    """
    可验证卖家，负责生成数据并创建注册包以提交给市场验证服务

    包含数据、数据哈希、公钥和零知识证明（ZKP），通过 ZKP，卖家可以证明自己拥有数据的私钥，而无需直接暴露私钥
    """

    def __init__(self, seller_id):
        self.id = seller_id
        self.private_key, self.public_key = generate_keys()
        self.data = None
        print(
            f"  Created Seller '{self.id}' with public key {self.public_key.to_string().hex()[:10]}..."
        )

    def set_data(self, data_stream):
        """设置卖家的数据流"""
        self.data = data_stream

    def get_data_registration_package(self):
        """
        创建一个包含数据、数据哈希、公钥和零知识证明（ZKP）的注册包，该包将提交给市场进行验证
        Returns:
            dict: 包含卖家ID、数据、数据哈希、公钥和ZKP的注册包
        """
        if self.data is None:
            raise ValueError("Seller data has not been set.")

        # 使用 SHA-256 哈希算法计算数据的哈希值
        data_hash = hashlib.sha256(self.data.tobytes()).digest()

        # 使用私钥对数据哈希进行签名
        signature = sign(self.private_key, data_hash)

        # 生成零知识证明（ZKP），证明卖家拥有数据的私钥
        zkp = generate_zkp_of_signature(data_hash, signature, self.public_key)

        return {
            "seller_id": self.id,
            "data": self.data,
            "data_hash": data_hash,
            "public_key": self.public_key,
            "zkp": zkp,
        }


class BuyerWithCredentials:
    """买家类，代表一个持有凭证的买家，可以参与市场交易"""

    def __init__(self, buyer_id, true_valuation):
        self.id = buyer_id
        self.mu_n = true_valuation
        # 这里的数字钱包可以存储不同类型的凭证
        self.wallet = {}
        print(f"  Created Buyer '{self.id}'.")

    def add_credential(self, credential_type, credential_object):
        """添加凭证到买家的数字钱包"""
        self.wallet[credential_type] = credential_object
        print(f"    Buyer '{self.id}' received credential of type '{credential_type}'.")

    def present_credential(self, credential_type):
        """展示买家持有的凭证"""
        return self.wallet.get(credential_type)
