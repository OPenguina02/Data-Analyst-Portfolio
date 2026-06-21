import pandas as pd

products = [
    # product_id,
    # product_name,
    # min_amount, max_amount,
    # min_interest_rate, max_interest_rate,
    # min_tenor_month, max_tenor_month,
    # penalty_rate

    [1, "Motorcycle Pawn Loan",
     300, 3000,
     1.8, 3.5,
     3, 24,
     1.0],

    [2, "Smartphone Pawn Loan",
     100, 1000,
     2.5, 5.0,
     3, 12,
     1.0],

    [3, "Gold Pawn Loan",
     100, 5000,
     1.2, 2.5,
     3, 12,
     1.0],

    [4, "Car Pawn Loan",
     2000, 20000,
     1.5, 3.0,
     6, 48,
     1.0],

    [5, "SME Business Loan",
     5000, 50000,
     2.0, 4.0,
     6, 60,
     1.5],

    [6, "Startup Business Loan",
     2000, 20000,
     3.0, 6.0,
     6, 36,
     2.0]
]

product_df = pd.DataFrame(
    products,
    columns=[
        "product_id",
        "product_name",
        "min_amount",
        "max_amount",
        "min_interest_rate",
        "max_interest_rate",
        "min_tenor_month",
        "max_tenor_month",
        "penalty_rate"
    ]
)

product_df["active_flag"] = True

product_df.to_csv("product.csv", index=False)

print(product_df)