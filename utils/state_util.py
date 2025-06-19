from fastapi import HTTPException
from fastapi import Request

def get_state_repos(request: Request):
    repos = request.state.repos
    if repos is None:
        raise HTTPException(status_code=500, detail="Repositories not initialized in request state")
    return repos