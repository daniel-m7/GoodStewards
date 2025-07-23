

import csv
import os
import requests
import time
from typing import Dict, Any, Optional

# --- Configuration ---
BASE_URL = "http://127.0.0.1:8000/api/v1"
CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'synthetic_data.csv'))
MAX_RETRIES = 5
RETRY_DELAY = 5  # seconds

# --- State Management ---
# In a real-world scenario, you would not store passwords like this.
# This is for demonstration purposes only.
user_passwords: Dict[str, str] = {}
user_tokens: Dict[str, str] = {}
created_orgs: Dict[str, Any] = {}
created_users: Dict[str, Any] = {}

def wait_for_api():
    """Waits for the API to be available."""
    print(f"Checking for API availability at {BASE_URL}...")
    for i in range(MAX_RETRIES):
        try:
            response = requests.get(f"{BASE_URL}/users/health-check")
            if response.status_code == 200:
                print("API is available.")
                return True
        except requests.ConnectionError:
            print(f"API not available, retrying in {RETRY_DELAY}s... ({i+1}/{MAX_RETRIES})")
            time.sleep(RETRY_DELAY)
    print("API did not become available. Exiting.")
    return False

def cleanup_database():
    """Cleans up all existing data from the database."""
    print("\n--- Phase 0: Cleaning Up Database ---")
    
    try:
        # Run the direct database cleanup script
        import subprocess
        import sys
        
        # Run the cleanup script
        result = subprocess.run([sys.executable, "cleanup_database.py"], 
                              capture_output=True, text=True, cwd=os.path.dirname(__file__))
        
        if result.returncode == 0:
            print("✅ Database cleanup completed successfully!")
        else:
            print(f"⚠ Database cleanup failed: {result.stderr}")
            
    except Exception as e:
        print(f"⚠ Could not run database cleanup: {e}")
    
    print("-" * 50)

def api_post(endpoint: str, data: Dict[str, Any], token: Optional[str] = None, files: Optional[Dict[str, Any]] = None) -> requests.Response:
    """Helper function to make POST requests and return response object."""
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    url = f"{BASE_URL}{endpoint}"
    print(f"POST {url}")
    try:
        if not files:
            response = requests.post(url, json=data, headers=headers)
        else:
            # When files are present, data should not be json-encoded
            response = requests.post(url, data=data, headers=headers, files=files)
        
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
        return requests.Response()

def api_put(endpoint: str, data: Dict[str, Any], token: Optional[str] = None) -> requests.Response:
    """Helper function to make PUT requests and return response object."""
    headers = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    
    url = f"{BASE_URL}{endpoint}"
    print(f"PUT {url}")
    try:
        response = requests.put(url, json=data, headers=headers)
        return response
    except requests.exceptions.RequestException as err:
        print(f"Request Error: {err}")
        return requests.Response()


def api_get_token(email: str, password: str) -> Optional[str]:
    """Logs in a user to get a JWT token."""
    data = {"username": email, "password": password}
    url = f"{BASE_URL}/auth/login"
    print(f"Attempting to get token for {email}...")
    
    try:
        # OAuth2 expects form data, not JSON
        response = requests.post(url, data=data)
        response.raise_for_status()
        token_data = response.json()
        token = token_data.get("access_token")
        user_tokens[email] = token
        print(f"Successfully got token for {email}")
        return token
    except requests.exceptions.HTTPError as err:
        print(f"Error getting token for {email}: {err}")
        print(f"Response Body: {err.response.text}")
    except requests.exceptions.RequestException as err:
        print(f"Request Error during token retrieval: {err}")
    return None

def process_row(row: Dict[str, Any]):
    """Processes a single row from the CSV file."""
    org_fein = row["organization_fein"]
    user_email = row["user_email"]

    # Skip if the user has already been processed
    if user_email in created_users:
        return

    password = "password123"  # Use a simple, consistent password
    user_passwords[user_email] = password

    # Determine if organization needs to be created or if user is joining
    if org_fein not in created_orgs:
        # This is the first user for this organization, so create the org
        registration_payload = {
            "full_name": row["user_full_name"],
            "email": user_email,
            "password": password,
            "organization": {
                "name": row["organization_name"],
                "fein": org_fein,
                "address": "123 Main St",
                "city": "Anytown",
                "state": "CA",
                "zip_code": "12345"
            }
        }
        print(f"Registering new user {user_email} and new organization '{row['organization_name']}'.")
        response = api_post("/auth/register", data=registration_payload)

        if response.status_code in [201, 409]: # 409 for race conditions is ok
            if response.status_code == 409:
                print(f"User or organization may already exist: {response.text}")
                # Attempt to fetch IDs to proceed
                org_id_response = requests.get(f"{BASE_URL}/organizations/fein/{org_fein}")
                if org_id_response.status_code != 200:
                    print(f"Could not retrieve existing org by FEIN. Skipping row.")
                    return
                org_id = org_id_response.json()["id"]
                user_id = "existing_user_id_placeholder" # Can't get this easily without another endpoint
            else:
                response_data = response.json()
                org_id = response_data["organization_id"]
                user_id = response_data["user_id"]
                print(f"New org created with ID: {org_id}, User ID: {user_id}")

            created_orgs[org_fein] = {"id": org_id, "name": row["organization_name"]}
            created_users[user_email] = {"id": user_id, "role": "treasurer", "org_fein": org_fein}
        else:
            print(f"Error registering user/org: {response.status_code} {response.text}")
            return
    else:
        # Organization already exists, so this user is joining
        org_id = created_orgs[org_fein]["id"]
        registration_payload = {
            "full_name": row["user_full_name"],
            "email": user_email,
            "password": password,
            "organization_id": org_id
        }
        print(f"Registering new user {user_email} for existing organization '{created_orgs[org_fein]['name']}'.")
        response = api_post("/auth/register", data=registration_payload)

        if response.status_code in [201, 409]:
            if response.status_code == 409:
                 print(f"User {user_email} may already exist: {response.text}")
                 user_id = "existing_user_id_placeholder"
            else:
                user_id = response.json()["user_id"]
                print(f"New user created with ID: {user_id}")

            created_users[user_email] = {"id": user_id, "role": row["user_role"], "org_fein": org_fein}
        else:
            print(f"Error registering user: {response.status_code} {response.text}")
            return


def run_submission_workflow(row: Dict[str, Any]):
    """Runs the receipt submission, approval, and payment workflow."""
    user_email = row["user_email"]
    password = user_passwords.get(user_email)
    org_fein = row["organization_fein"]

    if not password:
        print(f"Could not find password for {user_email}, skipping submission.")
        return

    print(f"\n--- Starting Receipt Submission Workflow for {user_email} ---")
    # Get user token
    user_token = user_tokens.get(user_email) or api_get_token(user_email, password)
    if not user_token:
        return

    # Prepare receipt data
    image_path = os.path.join(os.path.dirname(__file__), '..', 'data', os.path.basename(row["receipt_image_url"]))
    if not os.path.exists(image_path):
        print(f"Image not found at {image_path}, skipping receipt submission.")
        return

    receipt_data = {
        "vendor_name": row["receipt_vendor_name"],
        "total_amount": float(row["receipt_total_amount"]),
        "description": f"Receipt from {row['receipt_vendor_name']}"
    }

    with open(image_path, "rb") as f:
        files = {"image": (os.path.basename(image_path), f, "image/jpeg")}
        response = api_post("/receipts/upload", data=receipt_data, token=user_token, files=files)

    if response.status_code in [200, 201]:
        receipt = response.json()
        receipt_id = receipt["id"]
        print(f"User {user_email} submitted receipt ID: {receipt_id}")
        
        # 4. Treasurer Approves Receipt
        approve_receipt(org_fein, receipt_id)
    else:
        print(f"Error submitting receipt: {response.status_code} {response.text}")


def approve_receipt(org_fein: str, receipt_id: str):
    """Finds the treasurer for the org and has them approve the receipt."""
    print(f"--- Starting Approval Workflow for Receipt {receipt_id} ---")
    # Find the treasurer for the organization
    treasurer_email = None
    for email, user_data in created_users.items():
        if user_data.get("org_fein") == org_fein and user_data.get("role") == "treasurer":
            treasurer_email = email
            break
    
    if not treasurer_email:
        print(f"Could not find a treasurer for organization FEIN {org_fein}")
        return

    # Get treasurer token
    treasurer_password = user_passwords.get(treasurer_email)
    if not treasurer_password:
        print(f"Could not find password for treasurer {treasurer_email}")
        return
        
    treasurer_token = user_tokens.get(treasurer_email) or api_get_token(treasurer_email, treasurer_password)
    if not treasurer_token:
        return

    # Approve the receipt
    approval_data = {
        "payment_method": "Corporate Card",
        "payment_reference": f"PAY-{int(time.time())}"
    }
    response = api_put(f"/receipts/{receipt_id}/approve", data=approval_data, token=treasurer_token)
    if response.status_code == 200:
        print(f"Treasurer {treasurer_email} approved receipt ID: {receipt_id}")
        # 5. Treasurer Confirms Payment
        confirm_payment(treasurer_token, treasurer_email, receipt_id)
    else:
        print(f"Error approving receipt: {receipt_id}")


def confirm_payment(treasurer_token: str, treasurer_email: str, receipt_id: str):
    """Has the treasurer confirm payment for the receipt."""
    print(f"--- Starting Payment Confirmation for Receipt {receipt_id} ---")
    payment_data = {
        "payment_method": "Corporate Card",
        "confirmation_number": f"CONF-{int(time.time())}"
    }
    response = api_post(f"/receipts/{receipt_id}/confirm-payment", data=payment_data, token=treasurer_token)
    if response.status_code == 200:
        print(f"Treasurer {treasurer_email} confirmed payment for receipt ID: {receipt_id}")
    else:
        print(f"Error confirming payment for receipt ID: {receipt_id}")


def main():
    """Main function to run the data loading script."""
    if not wait_for_api():
        return

    # Clean up existing data first
    cleanup_database()

    if not os.path.exists(CSV_PATH):
        print(f"Error: CSV file not found at {CSV_PATH}")
        print("Please run `python generate_synthetic_data.py` first.")
        return

    with open(CSV_PATH, mode='r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        rows_to_process = [row for row in reader if row.get("user_email")]

    # Phase 1: Register all users and their organizations
    print("\n--- Phase 1: Registering All Users and Organizations ---")
    # Sort rows to ensure treasurers (who create orgs) are processed first
    rows_to_process.sort(key=lambda r: r['user_role'] != 'treasurer')
    for row in rows_to_process:
        process_row(row)
        time.sleep(0.2)  # Small delay to avoid overwhelming the server

    # Phase 2: Run the submission, approval, and payment workflows
    print("\n--- Phase 2: Running Submission, Approval, and Payment Workflows ---")
    for row in rows_to_process:
        if row["user_role"] == "member" and row.get("receipt_image_url"):
            # The user and org should exist now, this will trigger the workflow part
            run_submission_workflow(row)
            print("-" * 50)
            time.sleep(1)  # Delay between full workflow simulations

    print("\nScript finished.")


if __name__ == "__main__":
    main()
