
import pandas as pd
import numpy as np
import random

# =========================
# LOAD FILES
# =========================

customer_df = pd.read_csv("customer.csv", parse_dates=["customer_since_date"])
staff_df = pd.read_csv("staff.csv", parse_dates=["hire_date", "termination_date"])
sbh_df = pd.read_csv("staff_branch_history.csv", parse_dates=["start_date", "end_date"])
product_df = pd.read_csv("product.csv")
policy_df = pd.read_csv("policy.csv", parse_dates=["effective_date", "expiry_date"])
policy_product_df = pd.read_csv("policy_product.csv")
policy_branch_df = pd.read_csv("policy_branch.csv", parse_dates=["effective_date", "expiry_date"])

# =========================
# CONFIG
# =========================

YEAR_WEIGHTS = [15,20,30,35]

PRODUCT_WEIGHTS = {
    1: 30,
    2: 25,
    3: 20,
    4: 10,
    5: 10,
    6: 5
}

DEFAULT_RATE = {
    1: 0.10,
    2: 0.12,
    3: 0.03,
    4: 0.06,
    5: 0.08,
    6: 0.15
}

PAWN_PRODUCTS = [1, 2, 3, 4]
BUSINESS_PRODUCTS = [5, 6]

TENOR_STEP = {
    1: 3,
    2: 3,
    3: 3,
    4: 3,
    5: 6,
    6: 6

}

# =========================
# STAFF WEIGHT
# =========================

today = pd.Timestamp("2025-12-31")

staff_df["termination_date"] = pd.to_datetime(
    staff_df["termination_date"], errors="coerce"
)

staff_df["tenure_days"] = (
    (today - staff_df["hire_date"]).dt.days
).clip(lower=30)

staff_df["experience_factor"] = (
    staff_df["tenure_days"] / staff_df["tenure_days"].max()
)

staff_df["performance_factor"] = np.random.lognormal(
    mean=0,
    sigma=0.6,
    size=len(staff_df)
)

staff_df["weight"] = (
    staff_df["experience_factor"]
    * staff_df["performance_factor"]
)

# =========================
# HELPERS
# =========================

def assign_loan_count():
    r = random.random()

    if r < 0.80:
        return 1
    elif r < 0.95:
        return 2
    elif r < 0.99:
        return 3
    else:
        return random.randint(4, 6)

def random_date():
    year = random.choices(
        [2022, 2023, 2024, 2025],
        weights=YEAR_WEIGHTS,
        k=1
    )[0]

    start = pd.Timestamp(f"{year}-01-01")
    end = pd.Timestamp(f"{year}-12-31")

    return start + pd.Timedelta(
        days=random.randint(0, (end-start).days)
    )

def get_active_staff(loan_date):
    active = staff_df[
        (staff_df["hire_date"] <= loan_date)
        &
        (
            staff_df["termination_date"].isna()
            |
            (staff_df["termination_date"] >= loan_date)
        )
    ]
    return active

def get_branch(staff_id, loan_date):
    rows = sbh_df[
        (sbh_df["staff_id"] == staff_id)
        & (sbh_df["start_date"] <= loan_date)
        & (
            sbh_df["end_date"].isna()
            | (sbh_df["end_date"] >= loan_date)
        )
    ]

    if len(rows) == 0:
        return None

    return int(rows.iloc[0]["branch_id"])

def choose_product(customer_type):

    if customer_type == "INDIVIDUAL":
        pool = product_df[
            product_df["product_id"].isin(PAWN_PRODUCTS)
        ].copy()

    else:
        pool = product_df[
            product_df["product_id"].isin(BUSINESS_PRODUCTS)
        ].copy()

    weights = [
        PRODUCT_WEIGHTS[int(pid)]
        for pid in pool["product_id"]
    ]

    return pool.sample(
        n=1,
        weights=weights
    ).iloc[0]

def choose_policy(branch_id, product_id, loan_date):

    branch_policy = policy_branch_df[
        (policy_branch_df["branch_id"] == branch_id)
        & (policy_branch_df["effective_date"] <= loan_date)
        & (policy_branch_df["expiry_date"] >= loan_date)
    ]

    if len(branch_policy) == 0:
        return 1

    valid_ids = set(branch_policy["policy_id"])

    product_policy = policy_product_df[
        (policy_product_df["product_id"] == product_id)
        & (policy_product_df["policy_id"].isin(valid_ids))
    ]

    if len(product_policy) == 0:
        return 1

    return int(random.choice(
        product_policy["policy_id"].tolist()
    ))

# =========================
# PRIMARY STAFF
# =========================

staff_weights = staff_df["weight"] / staff_df["weight"].sum()

primary_staff = {}

for cid in customer_df["customer_id"]:
    primary_staff[cid] = np.random.choice(
        staff_df["staff_id"],
        p=staff_weights
    )

# =========================
# LOANS
# =========================

loans = []
loan_id = 1

for _, cust in customer_df.iterrows():

    loan_count = assign_loan_count()

    prev_product = None
    prev_date = None

    for _ in range(loan_count):

        if prev_date is None:
            loan_date = random_date()
        else:
            loan_date = prev_date + pd.DateOffset(
                months=random.randint(3,18)
            )

            if loan_date > pd.Timestamp("2025-12-31"):
                break

        active_staff = get_active_staff(loan_date)

        if len(active_staff) == 0:
            continue

        primary = primary_staff[cust["customer_id"]]

        if (
            primary in active_staff["staff_id"].values
            and random.random() < 0.85
        ):
            staff_id = primary
        else:
            weights = (
                active_staff["weight"]
                / active_staff["weight"].sum()
            )

            staff_id = np.random.choice(
                active_staff["staff_id"],
                p=weights
            )

        branch_id = get_branch(staff_id, loan_date)

        if branch_id is None:
            continue

        if prev_product is not None and random.random() < 0.60:
            product = prev_product
        else:
            product = choose_product(cust["customer_type"])

        prev_product = product
        prev_date = loan_date

        policy_id = choose_policy(
            branch_id,
            int(product["product_id"]),
            loan_date
        )

        pp = policy_product_df[
            (policy_product_df["policy_id"] == policy_id)
            & (policy_product_df["product_id"] == product["product_id"])
        ]

        min_amount = float(product["min_amount"])
        max_amount = float(product["max_amount"])
        min_rate = float(product["min_interest_rate"])
        max_rate = float(product["max_interest_rate"])

        if len(pp) > 0:
            row = pp.iloc[0]

            if pd.notna(row["min_amount_modifier"]):
                min_amount += row["min_amount_modifier"]

            if pd.notna(row["max_amount_modifier"]):
                max_amount += row["max_amount_modifier"]

            if pd.notna(row["min_interest_rate_modifier"]):
                min_rate += row["min_interest_rate_modifier"]

            if pd.notna(row["max_interest_rate_modifier"]):
                max_rate += row["max_interest_rate_modifier"]

        amount = round(
            np.random.triangular(
                min_amount,
                (min_amount + max_amount)/2,
                max_amount
            ),
            2
        )

        interest_rate = round(
            random.uniform(min_rate, max_rate),
            2
        )

        min_tenor = int(product["min_tenor_month"])
        max_tenor = int(product["max_tenor_month"])

        step = TENOR_STEP[
            int(product["product_id"])
        ]

        tenor = random.choice(
            list(range(min_tenor, max_tenor + 1, step))
        )

        product_id = int(product["product_id"])

        if random.random() < DEFAULT_RATE.get(
            int(product["product_id"]),
            0.1
        ):
            status = "DEFAULT"
        else:
            status = random.choice(
                ["ACTIVE", "CLOSED"]
            )

        if status == "CLOSED":
            outstanding = 0
        elif status == "ACTIVE":
            outstanding = round(
                amount * random.uniform(0.1,1.0),2
            )
        else:
            outstanding = round(
                amount * random.uniform(0.2,0.9),2
            )

        loans.append([
            loan_id,
            cust["customer_id"],
            int(staff_id),
            int(branch_id),
            int(product["product_id"]),
            policy_id,
            None,
            loan_date.date(),
            interest_rate,
            tenor,
            amount,
            outstanding,
            status
        ])

        loan_id += 1

loan_df = pd.DataFrame(
    loans,
    columns=[
        "loan_id",
        "customer_id",
        "staff_id",
        "branch_id",
        "product_id",
        "policy_id",
        "collateral_id",
        "start_date",
        "interest_rate",
        "tenor",
        "amount",
        "outstanding",
        "status"
    ]
)

loan_df.to_csv("loan.csv", index=False)

print("Loans:", len(loan_df))
print(loan_df.head())
