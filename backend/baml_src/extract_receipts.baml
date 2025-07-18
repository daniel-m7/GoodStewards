// The BAML linter would be here if we had one.
// Defines the AI function for extracting structured data from a receipt image.

client GPT4Turbo {
  provider openai
}

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
  client GPT4Turbo
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
    - tax_rate: The rate of the tax.

    Image:
    {{ receipt }}
  "#
}


