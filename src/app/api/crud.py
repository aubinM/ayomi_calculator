from app.api.models import CalculatorSchema
from app.db import calculator, database
from datetime import datetime as dt
from app.api.functions import eval_polish_expr


async def post(payload: CalculatorSchema):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    result = eval_polish_expr(payload.calcul)
    query = calculator.insert().values(calcul=payload.calcul,
                                       result=result,
                                       created_date=created_date)
    return await database.execute(query=query)


async def get(id: int):
    query = calculator.select().where(id == calculator.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = calculator.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload=CalculatorSchema):
    created_date = dt.now().strftime("%Y-%m-%d %H:%M")
    query = (
        calculator.update().where(id == calculator.c.id).values(
            calcul=payload.calcul,
            result=payload.result,
            created_date=created_date)
        .returning(calculator.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = calculator.delete().where(id == calculator.c.id)
    return await database.execute(query=query)
