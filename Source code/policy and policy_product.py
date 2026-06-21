import pandas as pd

# =========================
# POLICY
# =========================

policy_df = pd.DataFrame([
    [1, "Standard Policy", "2022-01-01", "2026-12-31"],
    [2, "New Branch Launch", "2022-01-01", "2026-12-31"],
    [3, "High Value Customer", "2022-01-01", "2026-12-31"],
    [4, "Repeat Customer Reward", "2022-01-01", "2026-12-31"],
    [5, "SME Growth Program", "2022-01-01", "2026-12-31"],
    [6, "Startup Support Program", "2022-01-01", "2026-12-31"],
    [7, "Summer Student Campaign 2023", "2023-06-01", "2023-08-31"],
    [8, "Summer Student Campaign 2024", "2024-06-01", "2024-08-31"],
    [9, "Summer Student Campaign 2025", "2025-06-01", "2025-08-31"],
    [10, "Lunar New Year Campaign 2023", "2023-01-01", "2023-02-15"],
    [11, "Lunar New Year Campaign 2024", "2024-01-01", "2024-02-15"],
    [12, "Lunar New Year Campaign 2025", "2025-01-01", "2025-02-15"]
], columns=[
    "policy_id",
    "policy_name",
    "effective_date",
    "expiry_date"
])

# =========================
# POLICY_PRODUCT
# =========================

policy_product_df = pd.DataFrame([

    # policy_product_id, policy_id, product_id,
    # min_amount_mod, max_amount_mod,
    # min_rate_mod, max_rate_mod,
    # min_tenor_mod, max_tenor_mod

    # New Branch Launch
    [1, 2, 1, None, None, -0.50, -0.50, None, 3],
    [2, 2, 2, None, None, -0.50, -0.50, None, 3],
    [3, 2, 3, None, None, -0.50, -0.50, None, 3],

    # High Value Customer
    [4, 3, 4, None, 5000, -1.00, -1.00, None, 12],
    [5, 3, 5, None, 10000, -1.00, -1.00, None, 12],

    # Repeat Customer Reward
    [6, 4, 1, None, None, -0.50, -0.50, None, 6],
    [7, 4, 3, None, None, -0.50, -0.50, None, 6],

    # SME Growth Program
    [8, 5, 5, -2000, 25000, -0.30, -0.30, 6, 12],

    # Startup Support Program
    [9, 6, 6, -1000, 5000, -0.50, -0.50, 6, 6],

    # Summer Student Campaign
    [10, 7, 2, -50, None, -0.50, -0.50, None, None],
    [11, 8, 2, -50, None, -0.50, -0.50, None, None],
    [12, 9, 2, -50, None, -0.50, -0.50, None, None],

    # Lunar New Year Campaign
    [13, 10, 1, None, None, -0.80, -0.80, None, 3],
    [14, 10, 3, None, None, -0.80, -0.80, None, 3],
    [15, 10, 4, None, None, -0.80, -0.80, None, 3],

    [16, 11, 1, None, None, -0.80, -0.80, None, 3],
    [17, 11, 3, None, None, -0.80, -0.80, None, 3],
    [18, 11, 4, None, None, -0.80, -0.80, None, 3],

    [19, 12, 1, None, None, -0.80, -0.80, None, 3],
    [20, 12, 3, None, None, -0.80, -0.80, None, 3],
    [21, 12, 4, None, None, -0.80, -0.80, None, 3]

], columns=[
    "policy_product_id",
    "policy_id",
    "product_id",
    "min_amount_modifier",
    "max_amount_modifier",
    "min_interest_rate_modifier",
    "max_interest_rate_modifier",
    "min_tenor_month_modifier",
    "max_tenor_month_modifier"
])

policy_df.to_csv("policy.csv", index=False)
policy_product_df.to_csv("policy_product.csv", index=False)

print(policy_df.head())
print(policy_product_df.head())