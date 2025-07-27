import sys, json
import numpy as np
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)
from market_participants import VerifiableSeller

if __name__ == "__main__":
    try:
        model_id = sys.argv[1]
        file_path = sys.argv[2]

        # 加载数据
        df = pd.read_csv(file_path)
        # 仅保留数值型数据列，并删除含有 NaN 的行
        numeric_df = df.select_dtypes(include=['number']).dropna()
        data = numeric_df.values

        # 初始化卖家并设置数据
        seller = VerifiableSeller(seller_id=model_id)
        seller.set_data(data)

        # 生成注册包
        package = seller.get_data_registration_package()

        # 构造 JSON 返回
        result = {
            "model_id": model_id,
            "data_hash": package["data_hash"].hex(),
            "signature": package["signature"].hex(),  # 注意从 package 提取
            "zkp": json.dumps(package["zkp"]),         # 序列化整个 mock ZKP
            "public_key": package["public_key"].to_string().hex()
        }

        print(json.dumps(result))
    except Exception as e:
        logging.info(f"Created Seller '{self.id}' with public key {self.public_key.to_string().hex()[:10]}...")
        logging.info(f"[Crypto] Generating mock ZKP for data hash {data_hash.hex()[:10]}...")
        sys.exit(1)
