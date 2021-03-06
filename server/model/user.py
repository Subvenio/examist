import hashlib
import random
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.schema import Table
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property
from server.model.session import Session
from server.exc import LoginError, NotFound
from server.database import Model, db
from server.library.util import find
from server.model.institution import Institution
from server.model.comment import Comment
from server.model.like import Like
from server.library.model import Serializable

ALPHABET = "abcdefghijklmnopqrstuvwxyz1234567890"

user_courses = Table("user_courses", db.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("course_id", Integer, ForeignKey("course.id"))
)

class User(Model, Serializable):
    __tablename__ = "user"

    # Attributes
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String(length=64))
    salt = Column(String(length=20))

    # Foreign keys
    institution_id = Column(Integer, ForeignKey("institution.id"))

    # Relationships
    sessions = relationship("Session", backref="user")
    courses = relationship("Course", secondary=user_courses)

    class Meta:
        load_only = ("password", "salt")

    @hybrid_property
    def active_session(self):
        return find(self.sessions, lambda session: session.active)

    def __init__(self, name, email, password, institution=None):
        self.name = name
        self.email = email
        self.salt = User.generateSalt()
        self.password = User.hash(password, self.salt)

        domain = User.extract_domain(self.email)

        if not institution:
            # Raises not found if the institution isn't found
            institution = Institution.getBy(db.session, domain=domain)

        # Now we need to get the institution by their email
        self.institution_id = institution.id
    
    def login(self, password=None):
        """Log the current user instance in. This does 2 things:
            1. Compares the password.
            2. Creates new session.
        """
        if password:
            hash = User.hash(password, self.salt)

            if hash != self.password:
                raise LoginError(self.email)

        # Create session token
        return Session(self)

    def comment(self, entity, content, parent=None):
        comment = Comment(self, entity, content, parent)
        self.comments.append(comment)
        return comment

    def like(self, entity):
        self.likes.append(Like(self, entity))

    @staticmethod
    def extract_domain(email):
        """Extract the insititution (domain) from an email."""
        return email.split("@")[1]

    @staticmethod
    def hash(password, salt):
        return hashlib.sha256(password + salt).hexdigest()

    @staticmethod
    def generateSalt(length=20):
        return ''.join(random.choice(ALPHABET) for i in range(length))

