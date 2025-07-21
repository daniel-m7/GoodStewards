import uuid
from datetime import date, datetime
from enum import Enum
from typing import List, Optional, Dict, Any

from sqlmodel import Field, Relationship, SQLModel


class Role(str, Enum):
    member = "member"
    treasurer = "treasurer"


class SpecialUserType(str, Enum):
    anonymous_donor = "anonymous_donor"
    unknown_user = "unknown_user"
    one_time_donor = "one_time_donor"


class ReceiptStatus(str, Enum):
    processing = "processing"
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    paid = "paid"


class PaymentMethod(str, Enum):
    zelle = "zelle"
    check = "check"
    other = "other"


class TaxType(str, Enum):
    state = "state"
    county = "county"
    transit = "transit"
    food = "food"


class FeedbackCategory(str, Enum):
    testimony = "testimony"
    bug_report = "bug_report"
    feature_request = "feature_request"


class FeedbackStatus(str, Enum):
    submitted = "submitted"
    in_review = "in_review"
    resolved = "resolved"


class Organization(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(index=True)
    fein: Optional[str] = Field(default=None, unique=True)
    ntee_code: Optional[str] = Field(default=None)
    address: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    state: Optional[str] = Field(default=None)
    zip_code: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    users: List["User"] = Relationship(back_populates="organization")
    receipts: List["Receipt"] = Relationship(back_populates="organization")
    payment_transactions: List["PaymentTransaction"] = Relationship(back_populates="organization")
    feedback: List["Feedback"] = Relationship(back_populates="organization")


class User(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    full_name: str
    email: Optional[str] = Field(default=None, unique=True, index=True)  # Nullable for special users
    hashed_password: Optional[str] = Field(default=None)  # Nullable for special users
    role: Role = Field(default=Role.member)
    contact_telephone: Optional[str] = Field(default=None)
    is_special_user: bool = Field(default=False)
    special_user_type: Optional[SpecialUserType] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    organization_id: uuid.UUID = Field(foreign_key="organization.id")
    organization: Organization = Relationship(back_populates="users")
    receipts: List["Receipt"] = Relationship(back_populates="user")
    feedback: List["Feedback"] = Relationship(back_populates="user")


class Receipt(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    image_url: str
    vendor_name: Optional[str] = Field(default=None)
    purchase_date: Optional[date] = Field(default=None)
    county: Optional[str] = Field(default=None)
    subtotal_amount: Optional[float] = Field(default=None)
    tax_amount: Optional[float] = Field(default=None)
    total_amount: Optional[float] = Field(default=None)
    expense_category: Optional[str] = Field(default=None)
    status: ReceiptStatus = Field(default=ReceiptStatus.processing)
    is_donation: bool = Field(default=False)
    payment_method: Optional[PaymentMethod] = Field(default=None)
    payment_reference: Optional[str] = Field(default=None)
    payment_proof_url: Optional[str] = Field(default=None)
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    approved_at: Optional[datetime] = Field(default=None)

    user_id: uuid.UUID = Field(foreign_key="user.id")
    organization_id: uuid.UUID = Field(foreign_key="organization.id")

    user: User = Relationship(back_populates="receipts")
    organization: Organization = Relationship(back_populates="receipts")
    tax_breakdowns: List["ReceiptTaxBreakdown"] = Relationship(back_populates="receipt")
    payment_transaction: Optional["PaymentTransaction"] = Relationship(back_populates="receipt")


class ReceiptTaxBreakdown(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    tax_type: TaxType
    amount: float

    receipt_id: uuid.UUID = Field(foreign_key="receipt.id")
    receipt: Receipt = Relationship(back_populates="tax_breakdowns")


class PaymentTransaction(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    transaction_date: date
    amount: float
    reference_id: Optional[str] = Field(default=None)

    organization_id: uuid.UUID = Field(foreign_key="organization.id")
    organization: Organization = Relationship(back_populates="payment_transactions")

    receipt_id: Optional[uuid.UUID] = Field(default=None, foreign_key="receipt.id")
    receipt: Optional[Receipt] = Relationship(back_populates="payment_transaction")


class Feedback(SQLModel, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    category: FeedbackCategory
    description: str
    device_info: Optional[str] = Field(default=None)  # Store JSON as string
    status: FeedbackStatus = Field(default=FeedbackStatus.submitted)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    user_id: uuid.UUID = Field(foreign_key="user.id")
    organization_id: uuid.UUID = Field(foreign_key="organization.id")

    user: User = Relationship(back_populates="feedback")
    organization: Organization = Relationship(back_populates="feedback")
