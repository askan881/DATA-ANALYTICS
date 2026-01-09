import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import datetime, timedelta
import re

fake = Faker()
np.random.seed(42)
random.seed(42)

# Number of records
n = 300000

# BMW Models
models = {
    "BMW X1": 45000,
    "BMW X3": 55000,
    "BMW X5": 70000,
    "BMW 3 Series": 42000,
    "BMW 5 Series": 60000,
    "BMW i4": 65000,
    "BMW iX": 85000
}

# Country-City Mapping
locations = {
    "Germany": ["Munich", "Berlin", "Hamburg", "Frankfurt"],
    "USA": ["New York", "Los Angeles", "Chicago", "Dallas"],
    "India": ["Mumbai", "Bangalore", "Delhi", "Chennai"],
    "UK": ["London", "Manchester", "Birmingham"],
    "China": ["Beijing", "Shanghai", "Shenzhen"],
    "UAE": ["Dubai", "Abu Dhabi"]
}

region_map = {
    "Germany": "Europe",
    "UK": "Europe",
    "USA": "North America",
    "India": "Asia",
    "China": "Asia",
    "UAE": "Middle East"
}

variants = ["Petrol", "Diesel", "Electric"]
dealers = ["BMW AutoHub", "Premium Motors", "Elite BMW", "City Wheels"]
email_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com"]

# Country phone codes
country_codes = {
    "Germany": "+49",
    "USA": "+1",
    "India": "+91",
    "UK": "+44",
    "China": "+86",
    "UAE": "+971"
}

def create_email_from_name(full_name):
    """Create email from customer name"""
    # Clean the name - remove special characters, split into parts
    name_clean = re.sub(r'[^a-zA-Z\s]', '', full_name).strip()
    name_parts = name_clean.split()
    
    if len(name_parts) >= 2:
        # Take first name and last name
        first_name = name_parts[0].lower()
        last_name = name_parts[-1].lower()
        
        # Choose email format randomly
        format_choice = random.choice([1, 2, 3])
        
        if format_choice == 1:
            # first.last@domain
            email_local = f"{first_name}.{last_name}"
        elif format_choice == 2:
            # firstlast@domain
            email_local = f"{first_name}{last_name}"
        else:
            # first_initial.last@domain
            email_local = f"{first_name[0]}.{last_name}"
    else:
        # If only one name part
        first_name = name_parts[0].lower() if name_parts else "user"
        email_local = first_name
    
    # Add random numbers to some emails for uniqueness
    if random.random() < 0.3:  # 30% chance to add numbers
        email_local += f"{random.randint(1, 999)}"
    
    domain = random.choice(email_domains)
    return f"{email_local}@{domain}"

def create_phone_number(country):
    """Create proper phone number based on country"""
    phone_code = country_codes[country]
    
    if country == "India":
        # Indian format: +91 98765 43210
        return f"{phone_code} {random.randint(70000, 99999)}{random.randint(10000, 99999)}"
    elif country == "USA":
        # US format: +1 (123) 456-7890
        return f"{phone_code} ({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
    elif country == "Germany":
        # German format: +49 123 4567890
        return f"{phone_code} {random.randint(100, 999)} {random.randint(1000000, 9999999)}"
    elif country == "UK":
        # UK format: +44 7123 456789
        return f"{phone_code} {random.randint(7000, 7999)} {random.randint(100000, 999999)}"
    elif country == "China":
        # Chinese format: +86 138 1234 5678
        return f"{phone_code} {random.randint(100, 199)}{random.randint(1000, 9999)}{random.randint(1000, 9999)}"
    else:  # UAE
        # UAE format: +971 50 123 4567
        return f"{phone_code} {random.randint(50, 59)}{random.randint(100, 999)}{random.randint(1000, 9999)}"

# Create unique customer IDs
customer_ids = [f"CUST{10000 + i}" for i in range(n)]

# Generate data for all three entities
orders_data = []
customers_data = []
payments_data = []

for i in range(n):
    # Generate customer data first
    customer_id = customer_ids[i]
    country = random.choice(list(locations.keys()))
    city = random.choice(locations[country])
    
    # Generate customer name
    customer_name = fake.name()
    
    # Generate email from customer name
    email = create_email_from_name(customer_name)
    
    # Generate proper phone number based on country
    phone_number = create_phone_number(country)
    
    # Customer details
    customer_row = {
        "customer_id": customer_id,
        "customer_name": customer_name,
        "customer_age": np.random.randint(18, 75),
        "gender": random.choice(["Male", "Female"]),
        "email": email,
        "phone": phone_number,
        "country": country,
        "city": city,
        "region": region_map[country],
        "registration_date": fake.date_between(start_date='-5y', end_date='-3y')
    }
    customers_data.append(customer_row)
    
    # Generate multiple orders per customer (1-3 orders)
    num_orders = random.choices([1, 2, 3], weights=[0.7, 0.2, 0.1])[0]
    
    for order_num in range(num_orders):
        order_id = f"ORD{1000000 + len(orders_data)}"
        
        # Order details
        model = random.choice(list(models.keys()))
        base_price = models[model]
        price = base_price + np.random.randint(-5000, 8000)
        quantity = np.random.choice([1, 1, 1, 2, 3, -1])  # includes bad data
        
        order_row = {
            "order_id": order_id,
            "order_date": fake.date_between(start_date='-3y', end_date='today'),
            "customer_id": customer_id,
            "model": model,
            "variant": random.choice(variants),
            "price": price,
            "quantity": quantity,
            "dealer": random.choice(dealers)
        }
        
        # Add null values to orders (moderate level - 5-10%)
        if random.random() < 0.08:  # 8% chance for price to be null
            order_row["price"] = None
        if random.random() < 0.07:  # 7% chance for quantity to be null
            order_row["quantity"] = None
        if random.random() < 0.06:  # 6% chance for variant to be null
            order_row["variant"] = None
        if random.random() < 0.05:  # 5% chance for dealer to be null
            order_row["dealer"] = None
            
        orders_data.append(order_row)
        
        # Payment details (one payment per order)
        payment_types = ["Cash", "Loan", "Lease"]
        payment_type = random.choice(payment_types)
        
        # Generate payment status based on payment type
        if payment_type == "Cash":
            payment_status = random.choice(["Completed", "Completed", "Completed", "Pending"])  # Mostly completed
        elif payment_type == "Loan":
            payment_status = random.choice(["Completed", "In Progress", "Pending", "Delayed"])
        else:  # Lease
            payment_status = random.choice(["Active", "Completed", "Terminated", "Overdue"])
        
        payment_row = {
            "payment_id": f"PAY{1000000 + len(payments_data)}",
            "order_id": order_id,
            "customer_id": customer_id,
            "payment_type": payment_type,
            "payment_status": payment_status,
            "payment_date": order_row["order_date"]
        }
        
        # Add null values to payments (moderate level - 5-10%)
        if random.random() < 0.09:  # 9% chance for payment status to be null
            payment_row["payment_status"] = None
        if random.random() < 0.04:  # 4% chance for payment type to be null
            payment_row["payment_type"] = None
            
        payments_data.append(payment_row)

# Convert to DataFrames
orders_df = pd.DataFrame(orders_data)
customers_df = pd.DataFrame(customers_data)
payments_df = pd.DataFrame(payments_data)

# Add additional null values to customers (moderate level - 5-10%)
customers_df.loc[customers_df.sample(frac=0.08).index, "email"] = None
customers_df.loc[customers_df.sample(frac=0.07).index, "phone"] = None
customers_df.loc[customers_df.sample(frac=0.06).index, "customer_age"] = None
customers_df.loc[customers_df.sample(frac=0.05).index, "gender"] = None
customers_df.loc[customers_df.sample(frac=0.04).index, "city"] = None

# Verify email matches name for non-null emails
print("🔍 Verifying email-name matching...")
non_null_emails = customers_df[customers_df['email'].notnull()].copy()
matched_count = 0

for idx, row in non_null_emails.iterrows():
    customer_name = row['customer_name'].lower()
    email = row['email'].lower().split('@')[0]
    
    # Clean name parts
    name_parts = re.sub(r'[^a-z\s]', '', customer_name).split()
    
    if len(name_parts) >= 2:
        first_name = name_parts[0]
        last_name = name_parts[-1]
        
        # Check if email contains first and last name
        if (first_name in email and last_name in email) or \
           (first_name[0] in email and last_name in email) or \
           (first_name in email and last_name[0] in email):
            matched_count += 1

match_percentage = (matched_count / len(non_null_emails)) * 100
print(f"✅ {matched_count}/{len(non_null_emails)} emails match customer names ({match_percentage:.1f}%)")

# Save datasets
orders_df.to_csv("orders.csv", index=False)
customers_df.to_csv("customers.csv", index=False)
payments_df.to_csv("payments.csv", index=False)

print("\n✅ Datasets created successfully!")
print("\nOrders Dataset:")
print(f"Records: {len(orders_df)}")
print(f"Null values per column:")
print(orders_df.isnull().sum())

print("\nCustomers Dataset:")
print(f"Records: {len(customers_df)}")
print(f"Null values per column:")
print(customers_df.isnull().sum())
print("\nSample data with matching emails:")
sample_customers = customers_df.head(10).copy()
for idx, row in sample_customers.iterrows():
    if pd.notnull(row['email']):
        print(f"  Name: {row['customer_name']:30} | Email: {row['email']}")

print("\nPayments Dataset:")
print(f"Records: {len(payments_df)}")
print(f"Null values per column:")
print(payments_df.isnull().sum())

# Show relationship between tables
print("\n📊 Dataset Relationships:")
print(f"Orders ←→ Customers: Linked by 'customer_id'")
print(f"Orders ←→ Payments: Linked by 'order_id'")
print(f"Customers ←→ Payments: Linked by 'customer_id'")

# Show percentage of null values
print("\n📈 Data Quality Summary:")
print(f"Orders - Total null values: {orders_df.isnull().sum().sum()} ({orders_df.isnull().sum().sum()/(len(orders_df)*len(orders_df.columns))*100:.1f}%)")
print(f"Customers - Total null values: {customers_df.isnull().sum().sum()} ({customers_df.isnull().sum().sum()/(len(customers_df)*len(customers_df.columns))*100:.1f}%)")
print(f"Payments - Total null values: {payments_df.isnull().sum().sum()} ({payments_df.isnull().sum().sum()/(len(payments_df)*len(payments_df.columns))*100:.1f}%)")