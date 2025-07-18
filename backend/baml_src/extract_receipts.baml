// The BAML linter would be here if we had one.
// Defines the AI function for extracting structured data from a receipt image.



// Define the structured data model we want to extract.
class ReceiptData {
  vendor_name string
  purchase_date string
  county string
  subtotal_amount float
  tax_amount float
  total_amount float
  expense_category string @description("Categorize the expense based on the items. Examples: Food, Office Supplies, Travel, Utilities, etc.")
  is_donation bool
  tax_breakdowns TaxBreakdown[]
}

enum TaxType {
  State
  County
  Transit
  Food
} 

class TaxBreakdown {
  tax_type TaxType
  tax_rate float
  amount float
}

// Define the AI function.
// The implementation of this function will be handled by the BAML runtime,
// which will call the specified LLM provider (e.g., Google's Gemini).
function ExtractReceiptData(
  // Input is the receipt image.
  receipt: image
) -> ReceiptData {
  client CustomGPT4o
    prompt #"
        {{_.role("user")}}
        
        You are an expert in extracting structured data from images of receipts.
        But you are also an expert preparer of E585 for a non-profit organization in the USA.
        Your task is to extract the following details from the receipt image:
        - Total amount
        - Date of the transaction
        - Business name
        - Address of the business
        - County of the business 
        - Total tax amount 
        - State Sales Tax 
        - Food County Transit Sales Tax
        - Expense Category 
        - Tax Rate

        Extract details from this image of a receipt: {{ receipt }}

        The county name may need to be inferred from the address info extracted. 
        Example: 1005 Jeweled Crown Ct, Indian Trail, NC 28079, USA, so return Union County, NC, USA.

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
            "expense_category": "Food",
            "tax_rate": 0.05
        }
        ```

        Ensure that the output is in the specified JSON format and includes all relevant fields.
        {{ ctx.output_format }}
    "#
}

test Test_Receipt {
functions [ExtractReceiptData]
  args {
    receipt {
      url "https://github.com/daniel-m7/GoodStewards/raw/main/data/1-receipt.png"
    }
  }
}
