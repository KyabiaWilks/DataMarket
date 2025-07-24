import subprocess
import json

def run_command(args):
    """辅助函数，用于运行命令行并捕获输出"""
    result = subprocess.run(args, capture_output=True, text=True)
    if result.returncode!= 0:
        print("Error:", result.stderr)
    return result.stdout.strip()

# --- 编译和设置 (由市场或可信方执行一次) ---
print("1. 编译电路...")
run_command(["zokrates", "compile", "-i", "root.zok"])

print("2. 执行可信设置...")
run_command(["zokrates", "setup"])

# --- 证明生成 (由卖家执行) ---
# 卖家想要证明他知道 337 是 113569 的平方根
private_input_a = 337
public_input_b = 113569

print(f"3. 计算见证 (witness) for a={private_input_a}, b={public_input_b}...")
run_command(["zokrates", "compute-witness", "-a", str(private_input_a), str(public_input_b)])

print("4. 生成证明...")
run_command(["zokrates", "generate-proof"])

# 读取生成的证明文件
with open('proof.json', 'r') as f:
    proof_data = json.load(f)
print("证明已生成！")


# --- 证明验证 (由市场执行) ---
print("5. 验证证明...")
# 市场方只需要知道公开输入 (113569) 和证明本身
verification_result = run_command(["zokrates", "verify"])
print(f"验证结果: {verification_result}")