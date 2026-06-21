import pandas as pd
import random
from datetime import timedelta

# =========================
# LOAD DATA
# =========================

branch_df = pd.read_csv("branch.csv")
policy_df = pd.read_csv("policy.csv")

branch_df["open_date"] = pd.to_datetime(branch_df["open_date"])
policy_df["effective_date"] = pd.to_datetime(policy_df["effective_date"])
policy_df["expiry_date"] = pd.to_datetime(policy_df["expiry_date"])

# =========================
# GENERATE POLICY_BRANCH
# =========================

records = []
policy_branch_id = 1

for _, policy in policy_df.iterrows():

    policy_id = policy["policy_id"]

    # Campaign toàn hệ thống
    if (
        "Lunar New Year" in policy["policy_name"]
        or "Summer Student" in policy["policy_name"]
    ):
        selected_branches = branch_df["branch_id"].tolist()

    # Startup pilot
    elif "Startup" in policy["policy_name"]:
        selected_branches = random.sample(
            branch_df["branch_id"].tolist(),
            k=15
        )

    # SME expansion
    elif "SME" in policy["policy_name"]:
        selected_branches = random.sample(
            branch_df["branch_id"].tolist(),
            k=40
        )

    # New Branch Launch
    elif "New Branch" in policy["policy_name"]:

        eligible = branch_df[
            branch_df["open_date"]
            >= policy["effective_date"] - timedelta(days=180)
        ]

        if len(eligible) > 20:
            selected_branches = random.sample(
                eligible["branch_id"].tolist(),
                k=20
            )
        else:
            selected_branches = eligible["branch_id"].tolist()

    # Các policy khác
    else:
        selected_branches = random.sample(
            branch_df["branch_id"].tolist(),
            k=30
        )

    for branch_id in selected_branches:

        # 80% rollout ngay
        if random.random() < 0.8:

            effective_date = policy["effective_date"]
            expiry_date = policy["expiry_date"]

        # 20% rollout trễ
        else:

            delay_days = random.randint(30, 180)

            effective_date = (
                policy["effective_date"]
                + timedelta(days=delay_days)
            )

            expiry_date = (
                policy["expiry_date"]
                + timedelta(days=delay_days)
            )

        records.append([
            policy_branch_id,
            policy_id,
            branch_id,
            effective_date.date(),
            expiry_date.date()
        ])

        policy_branch_id += 1

# =========================
# EXPORT
# =========================

policy_branch_df = pd.DataFrame(
    records,
    columns=[
        "policy_branch_id",
        "policy_id",
        "branch_id",
        "effective_date",
        "expiry_date"
    ]
)

policy_branch_df.to_csv(
    "policy_branch.csv",
    index=False
)

print(policy_branch_df.head())
print(f"Rows generated: {len(policy_branch_df):,}")