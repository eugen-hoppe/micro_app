from enum import auto

from src.db.generic import EntityRelation, ManyGeneric, OneGeneric


# Relation Registration
# =====================
class ToOne(EntityRelation):
    SUBSCRIPTION = auto()

class ToMany(EntityRelation):
    ACCOUNTS = auto()


class Many(ManyGeneric):
    MEMBERSHIPS = auto()
    MEMBERS = auto()

    @staticmethod
    def to_one() -> "ToOne":
        return ToOne

    @staticmethod
    def to_many() -> "Many":
        return Many

class One(OneGeneric):
    PLAN = auto()
    OWNER = auto()

    @staticmethod
    def to_many() -> "ToMany":
        return ToMany

    @staticmethod
    def to_one() -> "One":
        return One
