from typing import List, Optional

from fastapi import FastAPI, Query

from api.index import Indexer
from api.model import Matches

indexer = Indexer()
app = FastAPI()


@app.on_event("shutdown")
async def shutdown_event():
    indexer.close()


@app.get("/", response_model=Matches)
async def policy_search(keywords: Optional[List[str]] = Query(None)):
    if not keywords:
        return {"matches": []}

    results = indexer.search(keywords)

    return {
        "matches": [
            {
                "similarity": result.score,
                "policyId": result['policy_id'],
                "policyTitle": result['policy_title'],
                "sectors": result['sectors']
            } for result in results
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
