from flask.cli import FlaskGroup
from myblog.app import app

cli = FlaskGroup(app)

if __name__ == "__main__":
    cli()