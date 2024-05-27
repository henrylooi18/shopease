from website import create_app, db
from website import db

app = create_app()


if __name__ == "__main__":
    app.app_context().push()
    #db.drop_all()

    app.run(debug=True)
