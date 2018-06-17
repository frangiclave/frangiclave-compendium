from enum import Enum

from sqlalchemy import Column, Integer, String, Enum as EnumType

from frangiclave.compendium.base import Base


class FileCategory(Enum):
    DECKS = 'decks'
    ELEMENTS = 'elements'
    LEGACIES = 'legacies'
    RECIPES = 'recipes'
    VERBS = 'verbs'


class FileGroup(Enum):
    CORE = 'core'
    MORE = 'more'


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True)
    category = Column(EnumType(FileCategory, name='file_category'))
    group = Column(EnumType(FileGroup, name='file_group'))
    name = Column(String)

    def __init__(self, category: FileCategory, group: FileGroup, name: str):
        self.category = category
        self.group = group
        self.name = name
