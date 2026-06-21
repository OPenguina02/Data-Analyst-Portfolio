import pandas as pd
import random
from datetime import datetime, timedelta
import numpy as np

NUM_CUSTOMERS = 20000

# =========================
# CATEGORIES
# =========================

occupations = [
    "Office Worker", "Manual Worker", "Freelancer", "Driver",
    "Student", "Teacher", "Healthcare Worker",
    "Family Business Owner", "Artist", "Retired/Unemployed"
]

industries = [
    "Retail", "Manufacturing", "F&B", "Construction",
    "Logistics", "Agriculture", "Technology",
    "Education", "Healthcare", "Entertainment/Services"
]

size_groups = ["Micro", "Small", "Medium", "Large"]

# =========================
# HELPERS
# =========================

def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

def random_phone():
    return f"09{random.randint(10000000, 99999999)}"

# =========================
# CUSTOMER BASE
# =========================

customers = []

for cid in range(1, NUM_CUSTOMERS + 1):

    customer_type = "INDIVIDUAL" if random.random() < 0.85 else "CORPORATE"

    customers.append([
        cid,
        customer_type,
        random_date(datetime(2022, 1, 1), datetime(2025, 12, 31)).date(),
        "ACTIVE"
    ])

customer_df = pd.DataFrame(customers, columns=[
    "customer_id",
    "customer_type",
    "customer_since_date",
    "status"
])

# =========================
# INDIVIDUAL
# =========================

individual_rows = []

for cid in customer_df[customer_df.customer_type == "INDIVIDUAL"]["customer_id"]:

    individual_rows.append([
        cid,
        f"First_{cid}",
        f"Last_{cid}",
        random_date(datetime(1980, 1, 1), datetime(2003, 12, 31)).date(),
        random.choice(occupations),
        round(random.uniform(200, 3000), 2),
        random_phone()
    ])

individual_df = pd.DataFrame(individual_rows, columns=[
    "customer_id",
    "first_name",
    "last_name",
    "date_of_birth",
    "occupation",
    "income",
    "phone"
])

# =========================
# CORPORATE
# =========================

corporate_rows = []

for cid in customer_df[customer_df.customer_type == "CORPORATE"]["customer_id"]:

    corporate_rows.append([
        cid,
        f"Company_{cid}",
        random.choice(["LLC", "JSC", "SME"]),
        random.choice(industries),
        random.choice(size_groups),
        random_phone()
    ])

corporate_df = pd.DataFrame(corporate_rows, columns=[
    "customer_id",
    "company_name",
    "company_type",
    "industry",
    "size_group",
    "phone"
])

# =========================
# EXPORT
# =========================

customer_df.to_csv("customer.csv", index=False)
individual_df.to_csv("individual_customer.csv", index=False)
corporate_df.to_csv("corporate_customer.csv", index=False)

print(customer_df.head())
print(individual_df.head())
print(corporate_df.head())

print("TOTAL:", len(customer_df))