// See https://docs.boundaryml.com/v2/ for more info

// The AI provider to use.
// We allow this to be overridden by the BAML_CLIENT environment variable.
client GPT4o {
  provider openai
  options {
    model gpt-4o
    api_key env.OPENAI_API_KEY
  }
}

// Define the enums for our data models
enum Status {
  Processing
  Pending
  Approved
  Rejected
  Paid
}

enum TaxType {
  State
  County
  Transit
  Food
}

// Define the data structures for the output
class TaxBreakdown {
  tax_type TaxType
  amount float
}
 
class ReceiptData {
  vendor_name string?
  purchase_date string? 
  county string?
  subtotal_amount float?
  tax_amount float?
  total_amount float?
  expense_category string?
  status Status
  tax_breakdowns TaxBreakdown[]
}

// Define the AI function to extract data from a receipt image
function ExtractReceiptData(receipt: image) -> ReceiptData {
  client GPT4o
  prompt #"
        You are an expert in extracting structured data from images of receipts.
        Your task is to extract the following details from the receipt image:
        - Vendor name
        - Purchase date
        - Vendor address
        - Vendor address county
        - Subtotal amount
        - Tax amount
        - Total amount
        - Expense Category 
        - Tax breakdowns (state, county, transit, food)

        Extract details from this image of a receipt: {{ receipt }}

        The county name may need to be inferred from the address info extracted. 

        Return the extracted data in the following JSON format:
        ```json
        {
            "total_amount": 123.45,
            "date": "2023-10-01",
            "business": "Example Business",
            "address": "123 Example St, City, State, ZIP",
            "county": "Example County",
            "total_sales_tax": 5.00,
            "state_tax": 2.50,
            "food_county_transit_tax": 1.50,
            "expense_category": "Food"
        }
        ```

        Ensure that the output is in the specified JSON format and includes all relevant fields.
        {{ ctx.output_format }}
    "#
}
