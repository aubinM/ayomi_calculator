from app.api import crud
from app.api.models import CalculatorDB, CalculatorSchema
from fastapi import APIRouter, HTTPException, Path
from typing import List
from datetime import datetime as dt
from app.api.functions import eval_polish_expr

router = APIRouter()


@router.post("/", response_model=CalculatorDB, status_code=201)
async def create_calculator(payload: CalculatorSchema):
    """
    Create a calculator.

    Args:
        payload (CalculatorSchema) :

    """
    calculator_id = await crud.post(payload)
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")

    result = eval_polish_expr(payload.calcul)

    response_object = {
        "id": calculator_id,
        "calcul": payload.calcul,
        "result": result,
        "created_date": created_date,
    }
    return response_object


@router.get("/{id}/", response_model=CalculatorDB)
async def read_calculator(
    id: int = Path(..., gt=0),
):
    """
    Get a calculator.

    Args:
        id (int) : Defaults to Path(..., gt=0)

    """
    calculator = await crud.get(id)
    if not calculator:
        raise HTTPException(status_code=404, detail="Calculator not found")
    return calculator


@router.get("/", response_model=List[CalculatorDB])
async def read_all_calculators():
    """
    Reads all the calculators from crud.resul
    """
    return await crud.get_all()


@router.delete("/{id}/", response_model=CalculatorDB)
async def delete_calculator(id: int = Path(..., gt=0)):
    """
    Delete a calculator by id

    Args:
        id (int) : Defaults to Path(..., gt=0)

    """
    calculator = await crud.get(id)
    if not calculator:
        raise HTTPException(status_code=404, detail="Calculator not found")
    await crud.delete(id)

    return calculator
