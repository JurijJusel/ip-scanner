from pathlib import Path
from fastapi import FastAPI
from routers import virustotal_router, abuseip_router

from dotenv import load_dotenv
load_dotenv(dotenv_path=Path(__file__).parent / '.env')


app = FastAPI()
app.include_router(virustotal_router.router)
app.include_router(abuseip_router.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", reload=True)
