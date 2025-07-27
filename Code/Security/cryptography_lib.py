import hashlib
from ecdsa import SigningKey, VerifyingKey, NIST256p

from zksk import Secret, DLRep
from zksk import utils
from zksk import DLRep
from zksk.expr import Secret, SecretValue
from zksk.utils import deserialize

# -------------------------------
# Part 1: ECDSA 数字签名
# -------------------------------

def generate_keys():
    """
    生成新的ECDSA私钥和公钥对
    Returns:
        tuple: 包含私钥和公钥的元组 (SigningKey, VerifyingKey)
    """
    private_key = SigningKey.generate(curve=NIST256p)
    public_key = private_key.verifying_key
    return private_key, public_key


def sign(private_key, data_hash):
    """
    使用私钥对数据哈希进行签名

    Args:
        private_key (SigningKey): 卖家的私钥
        data_hash (bytes): 要签名的数据的哈希值

    Returns:
        bytes: 签名后的数据
    """
    return private_key.sign(data_hash)


def verify_signature(public_key, signature, data_hash):
    """
    验证签名是否与数据哈希和公钥匹配

    Args:
        public_key (VerifyingKey): 卖家的公钥
        signature (bytes): 要验证的签名
        data_hash (bytes): 原始数据的哈希值

    Returns:
        bool: 如果签名有效，返回True；否则返回False
    """
    try:
        return public_key.verify(signature, data_hash)
    except Exception:
        return False


# ===============================================================
# 第二部分：模拟零知识证明 (ZKP) 的实现
# 在实际应用中，这将被专用的零知识证明 (ZKP) 框架所取代，例如 ZoKrates、Circom 或 zksk
# 其目标是在不泄露私钥的情况下，证明用户知晓与公钥对应的私钥
# ===============================================================


def generate_zkp_of_signature(data_hash, signature, public_key):
    """
    使用 zksk 构造“知道签名者私钥”的零知识证明。
    模拟离散对数知识证明：证明知道私钥 x，使得 pk = g^x
    """
    print("[ZKP] Generating ZKP with zksk...")

    # 构造随机 group generator 和私钥
    g = utils.make_generators(1)[0]
    x = Secret()  # 私钥保密
    h = g ** x.value  # 公钥（模拟）

    stmt = DLRep(h, x * g)
    proof = stmt.prove()

    return {
        "zkp_proof": proof.serialize(),
        "g": g.serialize(),
        "h": h.serialize()
    }

def verify_zkp(public_key, data_hash, zkp_dict):
    print("[ZKP] Verifying ZKP with zksk...")

    g = deserialize(zkp_dict["g"])
    h = deserialize(zkp_dict["h"])
    proof = DLRep(h, SecretValue(0) * g).proof_type.deserialize(zkp_dict["zkp_proof"])

    stmt = DLRep(h, SecretValue(0) * g)
    return stmt.verify(proof)