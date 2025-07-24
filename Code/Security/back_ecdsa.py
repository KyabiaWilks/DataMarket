from Code.Security.back_ecdsa import SigningKey, NIST256p
import hashlib

# --- 卖家方 ---

# 1. 生成密钥对
# SigningKey 是私钥，VerifyingKey 是公钥
private_key = SigningKey.generate(curve=NIST256p)
public_key = private_key.verifying_key

# 2. 准备数据并签名
# 在实际应用中，我们会对数据文件本身进行哈希
data = b"This is the data stream from Seller A."
data_hash = hashlib.sha256(data).digest()

# 使用私钥对哈希进行签名
signature = private_key.sign(data_hash)

print(f"公钥: {public_key.to_string().hex()}")
print(f"签名: {signature.hex()}")


# --- 市场/验证方 ---

# 3. 验证签名
# 市场方需要有卖家的公钥、原始数据（或其哈希）以及签名
try:
    # 使用公钥验证签名是否与数据哈希匹配
    is_valid = public_key.verify(signature, data_hash)
    if is_valid:
        print("\n验证成功：签名是真实的。")
except Exception as e:
    print(f"\n验证失败：{e}")