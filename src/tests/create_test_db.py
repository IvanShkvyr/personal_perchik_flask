import bcrypt
import os
import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Date, Boolean, Table
from sqlalchemy.orm import relationship

from config.config import BASE_DIR
from src.libs import constants
from src.repository.users import inc, create_user
from src.models import db
from src.models import Users, AddressBook


class SqliteDriver():
    def __init__(self):
        self.db_url = "sqlite:///" + str(BASE_DIR / "database" / "app.test.db.sqlite")
        self.engine = create_engine(self.db_url)

    def destroy(self):
        # pass
        os.remove(str(BASE_DIR / "database" / "app.test.db.sqlite"))


class DbNoSetupTestCase(unittest.TestCase):
    def get_db_driver(self):
        return SqliteDriver()

    def setUp(self) -> None:
        self.db_driver = self.get_db_driver()
        self.engine = self.db_driver.engine
        self.db_url = self.db_driver.db_url
        self.Base = declarative_base()

    def tearDown(self) -> None:
        self.db_driver.destroy()


class DbTestCase(DbNoSetupTestCase):
    def setUp(self) -> None:
        super(DbTestCase, self).setUp()
        db.Model.metadata.create_all(self.engine)
        self.session = sessionmaker(bind=self.engine)()

    def tearDown(self):
        self.session.commit()
        self.session.close()
        super(DbTestCase, self).tearDown()
    