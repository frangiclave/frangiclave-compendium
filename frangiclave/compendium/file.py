from enum import Enum

from sqlalchemy import Column, Integer, String, Enum as EnumType

from frangiclave.compendium.base import Base


class FileCategory(Enum):
    DECKS = 'decks'
    ELEMENTS = 'elements'
    LEGACIES = 'legacies'
    RECIPES = 'recipes'
    VERBS = 'verbs'


class File(Base):
    __tablename__ = 'file'

    id = Column(Integer, primary_key=True)
    category = Column(EnumType(FileCategory, name='file_category'))
    name = Column(String)

    def __init__(self, category: FileCategory, name: str):
        self.category = category
        self.name = name
