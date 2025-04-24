from enum import auto

from src.db.generic import OneToManyGeneric, ManyGeneric, OneGeneric


class OneToMany(OneToManyGeneric):
    SUBSCRIPTION = auto()  # 1
    SUBSCRIPTIONS = auto()  # n
    USER = auto()  # 1
    USERS = auto()  # n
    ACCOUNT = auto()  # 1
    ACCOUNTS = auto()  # n


class Many(ManyGeneric):
    MEMBERSHIPS = auto()  # n
    MEMBERS = auto()  # n

    @staticmethod
    def to_many() -> "Many":
        return Many

    @staticmethod
    def to_one() -> "OneToMany":
        return OneToMany


class One(OneGeneric):
    PLAN = auto()  # 1
    OWNER = auto()  # 1

    @staticmethod
    def to_one() -> "One":
        return One

    @staticmethod
    def to_many() -> "OneToMany":
        return OneToMany
