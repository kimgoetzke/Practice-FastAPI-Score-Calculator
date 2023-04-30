from fastapi import FastAPI

from src.presentation.company_controller import company_router
from src.presentation.score_controller import score_router
from src.presentation.country_controller import country_router
from src.db.db_setup import engine
from src.db.models import country, company, score

country.Base.metadata.create_all(bind=engine)
company.Base.metadata.create_all(bind=engine)
score.Base.metadata.create_all(bind=engine)

tags_metadata = [
    {
        "name": "key_endpoint",
        "description": "This is the key endpoint that provides the key functionality of this app."
    }
]

app = FastAPI(
    title="Altman Z-Score Application",
    description="This project was created to practice Python and FastAPI "
                "(and related technologies such as SQL Alchemy, Pydantic, and Alembic).",
    openapi_tags=tags_metadata,
    version="0.1.0",
    contact={
        "name": "Kim Goetzke",
    },
    license_info={
        "name": "MIT",
        "url": "https://www.mit.edu/~amini/LICENSE.md"
    }
)

app.include_router(company_router)
app.include_router(country_router)
app.include_router(score_router)
