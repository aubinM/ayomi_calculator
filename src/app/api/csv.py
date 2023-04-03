from app.api import crud
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import pandas as pd

router = APIRouter()


@router.get("/csv", tags=["csv"])
async def get_csv_data():
    datas = await crud.get_all()
    ids, calculs, results, created_dates = ([] for i in range(4))
    for row in datas:
        ids.append(row[0])
        calculs.append(row[1])
        results.append(row[2])
        created_dates.append(row[3])

    # dictionary of lists
    _dict = {
        "id": ids,
        "calcul": calculs,
        "result": results,
        "created_date": created_dates,
    }

    df = pd.DataFrame(_dict)
    return StreamingResponse(
        iter([df.to_csv(index=False)]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=data.csv"},
    )
