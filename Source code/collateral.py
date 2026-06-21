import pandas as pd
import numpy as np
import random
from datetime import timedelta
import os

# ====================== CONFIG ======================
random.seed(42)
np.random.seed(42)

INPUT_LOAN = 'loan.csv'
INPUT_CUSTOMER = 'customer.csv'
OUTPUT_COLLATERAL = 'collaterals_way2.csv'
OUTPUT_LOAN_UPDATED = 'loans_with_collateral_way2.csv'

# Collateral types
COLLATERAL_TYPES = ['Motorcycle', 'Smartphone', 'Car']

# Tỷ lệ tái sử dụng
REUSE_RATE = 0.15  # 25% collateral được dùng cho >=2 loans
MAX_COLLATERAL_PER_CUSTOMER = 3
# ===================================================

# Đọc dữ liệu
loan_df = pd.read_csv(INPUT_LOAN)
customer_df = pd.read_csv(INPUT_CUSTOMER)

print(f"Loaded {len(loan_df)} loans and {len(customer_df)} customers")

# Tạo collateral theo customer (tái sử dụng)
collaterals = []
collateral_id = 1

for customer_id in customer_df['customer_id'].unique():
    customer_loans = loan_df[loan_df['customer_id'] == customer_id].sort_values('start_date')
    if len(customer_loans) == 0:
        continue
    
    num_collateral = random.randint(1, min(MAX_COLLATERAL_PER_CUSTOMER, max(1, len(customer_loans)//2 + 1)))
    
    for _ in range(num_collateral):
        # Chọn loan đầu tiên để valuation
        base_loan = customer_loans.iloc[random.randint(0, len(customer_loans)-1)]
        
        collateral_value = round(base_loan['amount'] * random.uniform(0.65, 0.95), 2)
        valuation_date = pd.to_datetime(base_loan['start_date']) - timedelta(days=random.randint(1, 30))
        
        # Release date (có thể NULL)
        release_date = None
        if random.random() < 0.3:  # 30% có release
            release_date = valuation_date + timedelta(days=random.randint(180, 720))
        
        collaterals.append({
            'collateral_id': collateral_id,
            'customer_id': customer_id,
            'collateral_type': random.choice(COLLATERAL_TYPES),
            'collateral_value': collateral_value,
            'valuation_date': valuation_date.date(),
            'release_date': release_date.date() if release_date else None,
            'status': 'RELEASED' if release_date else 'ACTIVE'
        })
        collateral_id += 1

collateral_df = pd.DataFrame(collaterals)

# Backfill loan.collateral_id (Cách 2)
def assign_collateral_to_loan(row):
    cust_collaterals = collateral_df[collateral_df['customer_id'] == row['customer_id']]
    if len(cust_collaterals) == 0:
        return None
    
    loan_date = pd.to_datetime(row['start_date'])
    
    for _, coll in cust_collaterals.iterrows():
        val_date = pd.to_datetime(coll['valuation_date'])
        rel_date = pd.to_datetime(coll['release_date']) if pd.notna(coll['release_date']) else pd.Timestamp.max
        
        if val_date <= loan_date < rel_date:
            return coll['collateral_id']
    
    # Nếu không tìm thấy, lấy collateral gần nhất
    return cust_collaterals.iloc[0]['collateral_id']

loan_df['collateral_id'] = loan_df.apply(assign_collateral_to_loan, axis=1)

# Lưu file
collateral_df.to_csv(OUTPUT_COLLATERAL, index=False)
loan_df.to_csv(OUTPUT_LOAN_UPDATED, index=False)

print(f"✅ Generated {len(collateral_df):,} collaterals (Way 2 - Reuse)")
print(f"   - Updated loans with collateral_id → {OUTPUT_LOAN_UPDATED}")
print(f"   - Collateral file → {OUTPUT_COLLATERAL}")
print(f"   - Reuse rate: {REUSE_RATE*100}%")

# Kiểm tra
print("\nSample Collateral:")
print(collateral_df.head())