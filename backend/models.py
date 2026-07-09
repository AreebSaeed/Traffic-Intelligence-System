from pydantic import BaseModel

class PredictionRequest(BaseModel):

    road_type: int

    length: float

    lanes: float

    maxspeed: float

    temperature: float

    humidity: float

    rain: float

    wind_speed: float

    cloud_cover: float

    hour: int

    day: int

    month: int

    weekday: int

    is_weekend: int

    is_holiday: int

    school_peak: int

    office_peak: int

    event: int