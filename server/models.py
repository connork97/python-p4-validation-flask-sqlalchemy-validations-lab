from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('name')
    def validate_name(self, key, author_name):
        if not author_name or author_name == None:
            raise ValueError("Author name must be included")
        return author_name
    
    @validates('phone_number')
    def validate_phone(self, key, number):
        if len(number) != 10:
            raise ValueError("Phone number must be 10 digits.")
        return number

    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    # Add validations and constraints 

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    @validates('title', 'content', 'summary', 'category')
    def validate_post(self, key, string):
        if key == 'title':
            clickbait = ["Won't Believe", "Secret", "Top", "Guess"]
            if not string or string == None:
                raise ValueError("All posts must have a title.")
            if not any(substring in string for substring in clickbait):
                raise ValueError("Title must have clickbait.")
            return string
        if key == 'content':
            if len(string) < 250:
                raise ValueError("Content must be at least 250 characters long.")
            return string
        if key == 'summary':
            if len(string) >= 250:
                raise ValueError("Summary must be 250 characters maximum.")
            return string
        if key == 'category':
            if string != "Fiction" and string != "Non-Fiction":
                raise ValueError("Category must be Fiction or Non-Fiction.")
            return string


    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
