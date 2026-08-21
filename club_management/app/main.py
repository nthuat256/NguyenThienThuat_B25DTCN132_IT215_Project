from fastapi import FastAPI
from app.db.database import Base, engine
from app.models import activity, club, user

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get('/')
def get_root():
    return{
        'message': 'wellcome'
    }
