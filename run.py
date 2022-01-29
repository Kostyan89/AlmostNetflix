from project.config import DevelopmentConfig
from project.dao.models import Genre
from project.app import create_app, db

app = create_app(DevelopmentConfig)


@app.shell_context_processor
def shell():
    return {
        "db": db,
        "Genre": Genre,
    }
