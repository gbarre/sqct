from app import create_app
# from models import *

connex_app = create_app()
app = connex_app.app

if __name__ == "__main__":
    app.run(use_reloader=True)
