from fastapi import APIRouter

import pandas as pd

router = APIRouter()

roads = pd.read_csv("ml/datasets/roads_raw.csv")


@router.get("/roads")

def get_roads(limit: int = 100):

    return roads.head(limit).to_dict(orient="records")