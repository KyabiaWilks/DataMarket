# run_auction.py
import sys
import json
import numpy as np
from shared import ml_model, price_range
from RevenueDiver import RevenueDivider
from HonestAuction import HonestAuction
from DynamicPricer import DynamicPricer
from UCBPricer import UCBPricer
from rmse import gain_function_rmse, generate_data

import warnings
warnings.filterwarnings("ignore")

def run_auction(bid, model_id, task_data):
    # 可切换使用 DynamicPricer 或 UCBPricer
    whichPricer = 0
    price_range = (50, 500)

    # 初始化市场组件
    if whichPricer == 0:
        pricer = DynamicPricer(price_range=price_range, num_experts=20, learning_rate_delta=0.1)
    else:
        pricer = UCBPricer(price_range=price_range, num_experts=20, confidence_c=2.0)

    auction = HonestAuction(ml_model=ml_model, gain_function=gain_function_rmse)
    divider = RevenueDivider(ml_model=ml_model, gain_function=gain_function_rmse)

    # 模拟数据
    X, Y = generate_data(M=10, T=100)

    # 步骤 1: 市场定价
    p_n, chosen_index = pricer.choose_price()

    # 步骤 2 & 3: 买家到达并出价
    b_n = float(bid)

    # 步骤 4 & 5: 市场分配数据并计算预测增益
    gain = auction.get_prediction_gain(X, Y, p_n, b_n)

    # 步骤 6: 市场收取收益
    revenue_n = auction.calculate_revenue(X, Y, p_n, b_n)

    # 步骤 7: 更新价格模型
    if whichPricer == 0:
        pricer.update_weights(auction, X, Y, b_n)
    else:
        pricer.update_stats(chosen_index, revenue_n)

    # 步骤 8: Shapley 分配
    shapley_values = divider.shapley_robust(X, Y, K=50)
    if np.sum(shapley_values) > 0:
        allocation_ratios = shapley_values / np.sum(shapley_values)
    else:
        allocation_ratios = np.ones(X.shape) / X.shape

    seller_revenues = revenue_n * allocation_ratios
    seller_payouts = np.round(seller_revenues, 2).tolist()

    # 构造结果 JSON
    result = {
        "market_price_offered": round(p_n, 2),
        "your_bid": b_n,
        "prediction_gain_achieved": round(gain, 4),
        "cost_to_you": round(revenue_n, 2),
        "seller_payouts": seller_payouts,
    }

    return result

if __name__ == "__main__":
    try:
        args = sys.argv[1:]
        bid = float(args[0])
        model_id = args[1]
        task_data = args[2] if len(args) > 2 else "{}"

        output = run_auction(bid, model_id, task_data)
        print(json.dumps(output))
    except Exception as e:
        print(json.dumps({"error": str(e)}))
        sys.exit(1)
