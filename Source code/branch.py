import pandas as pd
import random
from datetime import datetime, timedelta

province_distribution = {
    "Province_001": 18,
    "Province_002": 15,
    "Province_003": 13,
    "Province_004": 11,
    "Province_005": 10,
    "Province_006": 9,
    "Province_007": 8,
    "Province_008": 7,
    "Province_009": 5,
    "Province_010": 4
}

branches = []
branch_id = 1

for province, n_branches in province_distribution.items():
    for _ in range(n_branches):
        open_date = datetime(2022, 1, 1) + timedelta(
            days=random.randint(0, 1460)
        )

        status = random.choices(
            ["Active", "Closed"],
            weights=[88, 12]
        )[0]

        close_date = None
        if status == "Closed":
            close_date = open_date + timedelta(
                days=random.randint(180, 900)
            )

        branches.append([
            branch_id,
            province,
            open_date.date(),
            close_date,
            status
        ])

        branch_id += 1

branch_df = pd.DataFrame(
    branches,
    columns=[
        "branch_id",
        "province_name",
        "open_date",
        "close_date",
        "status"
    ]
)

branch_df.to_csv("branch.csv", index=False)
print(branch_df.head())