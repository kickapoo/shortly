from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


class CRUDMixin(object):
    """Mixin that adds convenience methods for CRUD
       (create, read, update, delete) operations."""

    @classmethod
    def create(cls, **kwargs):
        """Create a new record and save it the database."""
        instance = cls(**kwargs)
        return instance.save()

    def update(self, commit=True, **kwargs):
        """Update specific fields of a record."""
        for attr, value in kwargs.items():
            setattr(self, attr, value)
        return commit and self.save() or self

    def save(self, commit=True):
        """Save the record."""
        db.session.add(self)
        if commit:
            db.session.commit()
        return self

    def delete(self, commit=True):
        """Remove the record from the database."""
        db.session.delete(self)
        return commit and db.session.commit()


class Model(CRUDMixin, db.Model):
    """Base model class that includes CRUD convenience methods."""

    __abstract__ = True


class WordList(Model):
    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(240), unique=True, nullable=False)
    active = db.Column(db.Boolean(), default=False,)
    first_letter = db.Column(db.String(2), nullable=False)

    @classmethod
    def create_word(cls, word):
        """Helper creation function"""
        first_letter = word[0]
        cls.create(word=word, first_letter=first_letter)
        return cls

    def __repr__(self):
        return '<Word %r>' % self.word


class ShortUrl(Model):
    # Note: db.String(2000), 2000 is the max char a url can have.
    # TODO: add reference for previous statement
    id = db.Column(db.Integer, primary_key=True)
    raw_url = db.Column(db.String(2000), nullable=False)
    raw_url_md5 = db.Column(db.String(2000), nullable=False)
    shorten_url = db.Column(db.String(20), unique=True, nullable=False)

    def __repr__(self):
        return '<ShortUrl %r>' % self.shorten_url
