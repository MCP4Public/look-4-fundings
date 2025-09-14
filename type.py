from pydantic import BaseModel
from datetime import date
from pydantic import Field


class PublicFunding(BaseModel):
    """
    Represents a public funding opportunity.

    This model contains essential information about a public funding source,
    including its name, URL, and application deadline.

    Attributes:
        name (str): The name or title of the funding opportunity
        url (HttpUrl): Direct web link to the funding details/application page
        deadline (date): The final date for submitting applications
    """

    title: str = Field(..., description="Title of the funding")
    url: str = Field(..., description="Direct link to the funding page")
    summary: str = Field(..., description="Summary of the funding")
    deadline: date = Field(..., description="Deadline of the funding")
    status: str = Field(..., description="Status of the funding")
    budget: str = Field(..., description="Budget of the funding")
    company_affinity: float = Field(
        default=100,
        description="Affinity of the company with the funding",
        ge=0,
        le=100,
    )
    won: bool = Field(default=False, description="Whether the grant was won or not")


class MyCompany(BaseModel):
    """
    Represents a company.

    This model contains essential information about a company,
    including its name, URL, and application deadline.
    """

    name: str = Field(..., description="Name of the company")
    url: str = Field(..., description="Direct link to the company original page")
    scope: str = Field(..., description="Scope of the company")
