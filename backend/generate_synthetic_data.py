import csv
import random
from faker import Faker
import os

# Initialize Faker
fake = Faker()

# Define the receipt images from the data directory
data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))
receipt_images = [f for f in os.listdir(data_dir) if f.endswith(('.png', '.jpg'))]

# Define the headers for the CSV file
headers = [
    "organization_name",
    "organization_fein",
    "user_full_name",
    "user_email",
    "user_role",
    "receipt_image_url",
    "receipt_vendor_name",
    "receipt_total_amount",
]

# Generate the synthetic data
data = []
for i in range(2):
    organization_name = fake.company()
    organization_fein = fake.ein()

    # Create a treasurer for the organization
    treasurer_name = fake.name()
    treasurer_email = f"treasurer@{organization_name.lower().replace(' ', '').replace(',', '')}.com"
    data.append(
        [
            organization_name,
            organization_fein,
            treasurer_name,
            treasurer_email,
            "treasurer",
            None,
            None,
            None,
        ]
    )

    # Create a couple of users for the organization
    for j in range(2):
        user_name = fake.name()
        user_email = f"user{j+1}@{organization_name.lower().replace(' ', '').replace(',', '')}.com"
        
        # Add user row without receipt info first
        data.append(
            [
                organization_name,
                organization_fein,
                user_name,
                user_email,
                "member",
                None,
                None,
                None,
            ]
        )

        # Create a couple of receipts for each user
        for _ in range(2):
            receipt_image_url = os.path.join(data_dir, random.choice(receipt_images)) if receipt_images else None
            receipt_vendor_name = fake.company()
            receipt_total_amount = round(random.uniform(10.0, 500.0), 2)
            # Add new row for each receipt
            data.append(
                [
                    organization_name,
                    organization_fein,
                    user_name,
                    user_email,
                    "member",
                    receipt_image_url,
                    receipt_vendor_name,
                    receipt_total_amount,
                ]
            )

# Write the data to a CSV file
output_csv_path = os.path.join(data_dir, "synthetic_data.csv")
with open(output_csv_path, "w", newline="") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    writer.writerows(data)

print(f"Successfully regenerated {output_csv_path} with local image paths.")