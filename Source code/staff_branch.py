import pandas as pd
import random
from datetime import timedelta

# =========================
# LOAD DATA
# =========================

staff_df = pd.read_csv("staff.csv")
branch_df = pd.read_csv("branch.csv")

staff_df["hire_date"] = pd.to_datetime(staff_df["hire_date"])
staff_df["termination_date"] = pd.to_datetime(
    staff_df["termination_date"],
    errors="coerce"
)

branch_ids = branch_df["branch_id"].tolist()

# =========================
# GENERATE STAFF_BRANCH_HISTORY
# =========================

records = []
history_id = 1

for _, staff in staff_df.iterrows():

    staff_id = staff["staff_id"]
    hire_date = staff["hire_date"]
    termination_date = staff["termination_date"]

    # 85% ở 1 branch, 12% ở 2 branch, 3% ở 3 branch
    r = random.random()

    if r < 0.85:
        num_branches = 1
    elif r < 0.97:
        num_branches = 2
    else:
        num_branches = 3

    selected_branches = random.sample(
        branch_ids,
        num_branches
    )

    current_start = hire_date

    for i in range(num_branches):

        branch_id = selected_branches[i]

        # Bản ghi cuối
        if i == num_branches - 1:

            end_date = (
                termination_date.date()
                if pd.notna(termination_date)
                else None
            )

        else:

            transfer_months = random.randint(6, 24)

            transfer_date = (
                current_start +
                timedelta(days=transfer_months * 30)
            )

            # Không được vượt ngày nghỉ việc
            if (
                pd.notna(termination_date)
                and transfer_date >= termination_date
            ):
                transfer_date = (
                    termination_date -
                    timedelta(days=1)
                )

            end_date = transfer_date.date()

        records.append([
            history_id,
            staff_id,
            branch_id,
            current_start.date(),
            end_date
        ])

        history_id += 1

        if i != num_branches - 1:
            current_start = transfer_date + timedelta(days=1)

history_df = pd.DataFrame(
    records,
    columns=[
        "staff_branch_history_id",
        "staff_id",
        "branch_id",
        "start_date",
        "end_date"
    ]
)

history_df.to_csv(
    "staff_branch_history.csv",
    index=False
)

print(history_df.head())
print(f"Rows generated: {len(history_df):,}")