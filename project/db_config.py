'''
    all the database settings comes in this class members
    the class members should be references directly of uses a static getter
'''


class Config:
    engine = "postgres"
    port = "5432"
    host_name = "localhost"
    db_name = "bordito_db"
    password = "12345"
    username = "bordito"
