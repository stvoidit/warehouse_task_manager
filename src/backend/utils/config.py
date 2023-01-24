from typing import TypedDict

import toml


class DatabaseConfig(TypedDict):
    host: str
    port: int
    db: str
    user: str
    password: str

class ServiceConfig(TypedDict):
    secret: str

class Config(TypedDict):
    database: DatabaseConfig
    service: ServiceConfig

def read_config(filename: str) -> Config:
    cnf = Config()
    with open(filename, encoding="utf-8") as f:
        cnf = Config(toml.loads(f.read()))
    return cnf
