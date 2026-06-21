import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# ====================== CONFIG ======================
random.seed(42)
np.random.seed(42)

INPUT_LOAN = 'loans_with_collateral_way2.csv'
INPUT_PRODUCT = 'product.csv'
OUTPUT_PAYMENT = 'loan_payment.csv'

# ===================================================

loan_df = pd.read_csv(INPUT_LOAN)
product_df = pd.read_csv(INPUT_PRODUCT)

print(f"Loaded {len(loan_df):,} loans and {len(product_df)} products")

payments = []
payment_id = 1

for _, loan in loan_df.iterrows():
    tenor = int(loan['tenor'])
    start_date = pd.to_datetime(loan['start_date'])
    product = product_df[product_df['product_id'] == loan['product_id']].iloc[0]
    
    monthly_interest_rate = product['min_interest_rate'] / 100 / 12
    principal_per_month = loan['amount'] / tenor
    amount_due_base = round(principal_per_month + (loan['amount'] * monthly_interest_rate), 2)
    
    is_default_loan = loan['status'] == 'DEFAULT'
    default_installment = random.randint(max(3, tenor//2), tenor) if is_default_loan else None
    
    for i in range(1, tenor + 1):
        due_date = start_date + timedelta(days=30 * i)
        
        if is_default_loan and i >= default_installment:
            # Default loans: từ kỳ default trở đi chủ yếu missed
            payment_date = None
            amount_paid = 0.0
            penalty = 0.0
            status = 'MISSED'
        else:
            rand = random.random()
            if rand < 0.68:          # ON_TIME
                payment_date = due_date
                amount_paid = amount_due_base
                penalty = 0.0
                status = 'ON_TIME'
            elif rand < 0.88:        # LATE
                payment_date = due_date + timedelta(days=random.randint(5, 25))
                amount_paid = amount_due_base
                penalty = round(amount_due_base * (product['penalty_rate'] / 100) * (payment_date - due_date).days / 30, 2)
                status = 'LATE'
            elif rand < 0.96:        # PARTIAL
                payment_date = due_date + timedelta(days=random.randint(3, 20))
                amount_paid = round(amount_due_base * random.uniform(0.45, 0.92), 2)
                penalty = round((amount_due_base - amount_paid) * (product['penalty_rate'] / 100) * 0.8, 2)
                status = 'PARTIAL'
            else:                    # MISSED
                payment_date = None
                amount_paid = 0.0
                penalty = 0.0
                status = 'MISSED'
        
        payments.append({
            'payment_id': payment_id,
            'loan_id': int(loan['loan_id']),
            'installment_no': i,
            'due_date': due_date.date(),
            'payment_date': payment_date.date() if payment_date else None,
            'amount_due': amount_due_base,
            'amount_paid': round(amount_paid, 2),
            'penalty': round(penalty, 2),
            'payment_status': status
        })
        payment_id += 1

payment_df = pd.DataFrame(payments)

# Lưu file
payment_df.to_csv(OUTPUT_PAYMENT, index=False)

print(f"✅ Hoàn thành! Generated {len(payment_df):,} payment records")
print(f"   File: {OUTPUT_PAYMENT}")
print("\nTóm tắt Payment Status:")
print(payment_df['payment_status'].value_counts())

# Kiểm tra nhanh
print("\nSample 10 records:")
print(payment_df.head(10))