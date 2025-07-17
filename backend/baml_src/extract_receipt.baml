// The BAML linter would be here if we had one.
// Defines the AI function for extracting structured data from a receipt image.

// Define the structured data model we want to extract.
class ReceiptData {
  vendor_name String
  purchase_date Date
  county String
  subtotal_amount Float
  tax_amount Float
  total_amount Float
  expense_category String @description("Categorize the expense based on the items. Examples: Food, Office Supplies, Travel, Utilities, etc.")
  is_donation Boolean
  tax_breakdowns TaxBreakdown[]
}

class TaxBreakdown {
  tax_type String @enum("state", "county", "transit", "food")
  amount Float
}

// Define the AI function.
// The implementation of this function will be handled by the BAML runtime,
// which will call the specified LLM provider (e.g., Google's Gemini).
function ExtractReceiptData(
  // Input is the receipt image.
  receipt: image
) -> ReceiptData {
  // The prompt for the LLM is defined here.
  prompt #"
    Analyze the following receipt image and extract the data into a structured JSON format according to the defined schema.

    - vendor_name: The name of the store or vendor.
    - purchase_date: The date of the purchase.
    - county: The county where the purchase was made. If not explicitly mentioned, infer from the city or store location if possible.
    - subtotal_amount: The subtotal before taxes.
    - tax_amount: The total amount of all taxes.
    - total_amount: The final total amount.
    - expense_category: The category of the expense.
    - is_donation: Set to true if the receipt is for a donation, otherwise false.
    - tax_breakdowns: A list of all individual taxes (state, county, transit, food) and their amounts.

    Image:
    {{ receipt }}
  "#
}
