#!/usr/bin/env python3
"""
DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError

from user import Base, User


class DB:
    """
    DB class
    """

    def __init__(self) -> None:
        """
        Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """
        Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> None:
        """
        Add a new user to the database
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find the first user that matches the given keyword arguments.

        Args:
            **kwargs: Arbitrary keyword arguments used for filtering.

        Returns:
            User: The first user found that matches the given filters.

        Raises:
            NoResultFound: If no user is found that matches the filters.
            InvalidRequestError: If the query has invalid arguments.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except TypeError:
            raise InvalidRequestError

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update the user with the given user_id
        using the provided keyword arguments.
        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments used
            for updating the user's attributes.

        Returns:
            None

        Raises:
            ValueError: If an invalid attribute is provided.
            NoResultFound: If no user is found with the given user_id.
        """
        valid_attributes = {
            "email",
            "hashed_password",
            "session_id",
            "reset_token"
            }

        try:
            user = self.find_user_by(id=user_id)

            for key, value in kwargs.items():
                if key in valid_attributes:
                    setattr(user, key, value)
                else:
                    raise ValueError(f"Invalid attribute: {key}")

            self._session.commit()

        except NoResultFound:
            raise NoResultFound(f"No user found with id: {user_id}")
