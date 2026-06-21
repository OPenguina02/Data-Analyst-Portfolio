import pandas as pd
import os

print("🔍 BẮT ĐẦU DATA QUALITY ASSURANCE\n")

# Danh sách file thực tế của bạn
files = {
    'branch': 'branch.csv',                    # sửa chính tả nếu cần
    'product': 'product.csv',
    'policy': 'policy.csv',
    'policy_product': 'policy_product.csv',
    'policy_branch': 'policy_branch.csv',
    'staff': 'staff.csv',
    'staff_branch_history': 'staff_branch_history.csv',
    'customer': 'customer.csv',
    'individual_customer': 'individual_customer.csv',
    'corporate_customer': 'corporate_customer.csv',
    'loan': 'loan.csv',
    'loan_backfill': 'loans_with_collateral_way2.csv',
    'collateral': 'collaterals_way2.csv',        # giả sử tên này
    'payment': 'loan_payment.csv'
}

data = {}
for name, file in files.items():
    if os.path.exists(file):
        data[name] = pd.read_csv(file)
        print(f"✓ Loaded {name}: {len(data[name]):,} records")
    else:
        print(f"⚠️ Missing file: {file}")

print("\n" + "="*80)

# ====================== CHECKS ======================
print("1. Referential Integrity:")

# Customer hierarchy
if 'customer' in data and 'individual_customer' in data:
    print(f"   Customer → Individual: {'✅ OK' if set(data['individual_customer']['customer_id']).issubset(set(data['customer']['customer_id'])) else '❌ Error'}")

if 'customer' in data and 'corporate_customer' in data:
    print(f"   Customer → Corporate: {'✅ OK' if set(data['corporate_customer']['customer_id']).issubset(set(data['customer']['customer_id'])) else '❌ Error'}")

# Loan checks
if 'loan' in data and 'customer' in data:
    print(f"   Loan → Customer: {'✅ OK' if set(data['loan']['customer_id']).issubset(set(data['customer']['customer_id'])) else '❌ Error'}")

if 'loan_backfill' in data and 'collateral' in data:
    coll_set = set(data['collateral']['collateral_id'])
    loan_coll = set(data['loan_backfill']['collateral_id'].dropna())
    print(f"   Loan (backfill) → Collateral: {'✅ OK' if loan_coll.issubset(coll_set) else '❌ Error'}")

if 'payment' in data and 'loan' in data:
    print(f"   Payment → Loan: {'✅ OK' if set(data['payment']['loan_id']).issubset(set(data['loan']['loan_id'])) else '❌ Error'}")

print("\n2. Business Rules:")
if 'loan_backfill' in data:
    df_loan = data['loan_backfill']
    print(f"   Total Loans: {len(df_loan):,}")
    print(f"   Default Rate: {(df_loan['status'] == 'DEFAULT').mean()*100:.2f}%")

if 'payment' in data and 'loan_backfill' in data:
    avg_pay = len(data['payment']) / len(data['loan_backfill'])
    print(f"   Avg payments per loan: {avg_pay:.2f}")

print("\n3. Missing Values:")
for name, df in data.items():
    miss = df.isnull().sum().sum()
    if miss > 0:
        print(f"   {name}: {miss} missing values")

print("\n🎉 QA Check hoàn tất.")