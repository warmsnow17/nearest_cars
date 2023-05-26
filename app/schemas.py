from typing import List, Optional

from pydantic import BaseModel


class CargoCreate(BaseModel):
    pick_up_location: int
    delivery_location: int
    weight: int
    description: str


class CargoOut(BaseModel):
    id: int
    pick_up_location: str
    delivery_location: str
    weight: int
    description: str


class CargoListOut(BaseModel):
    id: int
    pick_up_location: str
    delivery_location: str
    nearest_trucks_count: int


class TruckDistance(BaseModel):
    unique_number: str
    distance: float


class CargoDetailOut(BaseModel):
    id: int
    pick_up_location: str
    delivery_location: str
    weight: int
    description: str
    all_trucks: List[TruckDistance]


class TruckUpdate(BaseModel):
    zip_code: int


class CargoUpdate(BaseModel):
    weight: Optional[int] = None
    description: Optional[str] = None


class CargoUpdateListOut(BaseModel):
    id: int
    weight: int
    description: str
