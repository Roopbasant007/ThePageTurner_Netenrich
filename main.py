from api.create_app import create_app
import uvicorn
from pathlib import Path
import os




app = create_app()


# PORT = environ.get('PORT', 3000)
# DEBUG = environ.get('DEBUG', False)

if __name__ == "__main__":
    uvicorn.run(app,host = "127.0.0.1" ,port = 8000)