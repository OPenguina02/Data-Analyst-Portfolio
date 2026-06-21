import pandas as pd
import random
from datetime import datetime, timedelta

NUM_STAFF = 1000

def random_date(start, end):
    return start + timedelta(
        days=random.randint(0, (end - start).days)
    )

staff_data = []

for staff_id in range(1, NUM_STAFF + 1):

    dob = random_date(
        datetime(1980, 1, 1),
        datetime(2003, 12, 31)
    )

    hire_date = random_date(
        datetime(2022, 1, 1),
        datetime(2025, 12, 31)
    )

    termination_date = None

    # 18% nghỉ việc
    if random.random() < 0.18:

        max_term_date = datetime(2025, 12, 31)
        termination_start = hire_date + timedelta(days=30)

        if termination_start <= max_term_date:
            termination_date = random_date(
                termination_start,
                max_term_date
            ).date()

    phone = f"09{random.randint(10000000, 99999999)}"

    staff_data.append([
        staff_id,
        f"Staff_{staff_id:06d}",
        dob.date(),
        hire_date.date(),
        termination_date,
        phone
    ])

staff_df = pd.DataFrame(
    staff_data,
    columns=[
        "staff_id",
        "full_name",
        "date_of_birth",
        "hire_date",
        "termination_date",
        "phone"
    ]
)

staff_df.to_csv("staff.csv", index=False)

print(staff_df.head())
print(f"Total Staff: {len(staff_df):,}")
print(
    f"Terminated: "
    f"{staff_df['termination_date'].notna().sum():,}"
)