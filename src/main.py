from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import click
import sqlalchemy as sa

class Base(DeclarativeBase):
    pass


db = SQLAlchemy(model_class=Base)


class User(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(sa.String, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)


class Card(db.Model):
    id: Mapped[int] = mapped_column(sa.Integer, primary_key=True)
    title: Mapped[str] = mapped_column(sa.String, nullable=False)
    user: Mapped[str] = mapped_column(sa.String, nullable=False)
    password: Mapped[str] = mapped_column(sa.String, nullable=False)
    desc: Mapped[str] = mapped_column(sa.String, nullable=True)
    user_id: Mapped[int] = mapped_column(sa.ForeignKey("user.id"))


    def __repr__(self) -> str:
        return f'Card:(id: {self.id!r}, title: {self.title!r}, author: {self.user_id!r})'


@click.command("init-db")
def init_db_command():
    global db
    click.echo("Initialized the database.")
    with current_app.app_context():
        db.create_all()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///passPro.sqlite"
    )

    if test_config is None:
        app.config.from_pyfile("config.py", silent=True)
    else:
        app.config.from_mapping(test_config)


    app.cli.add_command(init_db_command)


    db.init_app(app)

    from src.controller import user
    app.register_blueprint(user.app)

    return app
