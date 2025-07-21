import asyncio
import logging
from typing import Optional
from baml_client import b
from baml_client.types import ReceiptData, TaxBreakdown
from baml_py import Image

logger = logging.getLogger(__name__)

class BAMLService:
    """Service for BAML AI-powered receipt data extraction."""
    
    @staticmethod
    async def extract_receipt_data(image_data: bytes, content_type: str = "image/jpeg") -> Optional[ReceiptData]:
        """
        Extract structured data from a receipt image using BAML.
        
        Args:
            image_data: Raw image bytes
            content_type: MIME type of the image
            
        Returns:
            ReceiptData object if extraction successful, None otherwise
        """
        try:
            # Create BAML Image object from bytes
            import base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            image = Image.from_base64(content_type, image_base64)
            
            # Call BAML function for data extraction
            result = await b.ExtractReceiptData(receipt=image)
            
            return result
            
        except Exception as e:
            # Log the error using structured logging
            logger.error(f"BAML extraction failed: {str(e)}", exc_info=True)
            return None
    
    @staticmethod
    def validate_extracted_data(data: ReceiptData) -> bool:
        """
        Validate that extracted data meets minimum requirements.
        
        Args:
            data: Extracted receipt data
            
        Returns:
            True if data is valid, False otherwise
        """
        # Check for required fields
        if not data.vendor_name or not data.total_amount:
            return False
        
        # Validate amounts are positive
        if data.total_amount <= 0:
            return False
        
        # Validate tax breakdowns if present
        if data.tax_breakdowns:
            for breakdown in data.tax_breakdowns:
                if breakdown.amount < 0:
                    return False
        
        return True 