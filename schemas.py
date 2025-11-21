"""
Database Schemas for Kandy LK MVP

Each Pydantic model maps to a MongoDB collection (lowercased class name).
These are used for validation and by the admin database viewer.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, HttpUrl
from datetime import date


class User(BaseModel):
    """Basic user account (tourist)."""
    name: str = Field(..., description="Full name")
    email: str = Field(..., description="Email address")
    phone: Optional[str] = Field(None, description="Contact number")
    country: Optional[str] = Field(None, description="Country of residence")
    preferred_languages: Optional[List[str]] = Field(default_factory=list)


class Agency(BaseModel):
    name: str = Field(..., description="Agency name")
    description: Optional[str] = None
    logo_url: Optional[HttpUrl] = None
    website: Optional[HttpUrl] = None
    verified: bool = Field(False, description="Verification status")
    contact_email: Optional[str] = None
    contact_phone: Optional[str] = None
    base_location: Optional[str] = Field(None, description="City/area")


class Guide(BaseModel):
    full_name: str
    photo_url: Optional[HttpUrl] = None
    languages: List[str] = Field(default_factory=list)
    specializations: List[str] = Field(default_factory=list, description="e.g., culture, hiking, food")
    years_experience: int = Field(ge=0, default=0)
    bio: Optional[str] = None
    verified: bool = False
    rating: float = Field(ge=0, le=5, default=0)
    total_reviews: int = Field(ge=0, default=0)
    home_base: Optional[str] = Field(None, description="City/area guide is based in")
    agency_id: Optional[str] = Field(None, description="Reference to agency _id as string")
    day_rate_usd: Optional[float] = Field(None, ge=0)
    availability_notes: Optional[str] = None


class TourPackage(BaseModel):
    title: str
    description: Optional[str] = None
    duration_days: int = Field(ge=1)
    price_usd: float = Field(ge=0)
    tags: List[str] = Field(default_factory=list)
    guide_id: str = Field(..., description="Guide offering this package (_id as string)")
    locations: List[str] = Field(default_factory=list)


class Booking(BaseModel):
    user_name: str
    user_email: str
    guide_id: str
    package_id: Optional[str] = None
    start_date: date
    end_date: date
    party_size: int = Field(ge=1, default=1)
    notes: Optional[str] = None
    status: str = Field(default="pending", description="pending | confirmed | completed | cancelled")


class Review(BaseModel):
    guide_id: str
    booking_id: str
    rating: int = Field(ge=1, le=5)
    title: Optional[str] = None
    comment: Optional[str] = None
    photos: Optional[List[HttpUrl]] = Field(default_factory=list)


class Place(BaseModel):
    name: str
    description: Optional[str] = None
    region: Optional[str] = Field(None, description="Province/area")
    category: Optional[str] = Field(None, description="nature | culture | food | adventure | spiritual | other")
    coordinates: Optional[tuple] = Field(None, description="(lat, lng)")
    best_time: Optional[str] = None
    difficulty: Optional[str] = Field(None, description="easy | moderate | hard")
    tips: Optional[List[str]] = Field(default_factory=list)
    images: Optional[List[HttpUrl]] = Field(default_factory=list)


class Business(BaseModel):
    name: str
    type: str = Field(..., description="restaurant | shop | guesthouse | medical | other")
    description: Optional[str] = None
    location: Optional[str] = None
    coordinates: Optional[tuple] = None
    price_range: Optional[str] = Field(None, description="$ | $$ | $$$")
    opening_hours: Optional[str] = None
    phone: Optional[str] = None
    website: Optional[HttpUrl] = None
    images: Optional[List[HttpUrl]] = Field(default_factory=list)
    verified: bool = False
