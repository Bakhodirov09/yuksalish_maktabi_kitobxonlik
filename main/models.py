import sqlalchemy
from main.database_set import metadata

parents = sqlalchemy.Table(
    "parents",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("surname", sqlalchemy.String),
    sqlalchemy.Column("phone_number", sqlalchemy.String),
    sqlalchemy.Column("username", sqlalchemy.String),
    sqlalchemy.Column("farzandi", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("farzand_sinf", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("farzand_sinf_guruxi", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("who", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger)
)

classes = sqlalchemy.Table(
    "classes",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("class_number", sqlalchemy.String)
)

groups = sqlalchemy.Table(
    "groups",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("class_number", sqlalchemy.String),
    sqlalchemy.Column("group", sqlalchemy.String)
)

admins = sqlalchemy.Table(
    "admins",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger, nullable=True)
)

books = sqlalchemy.Table(
    "books",
    metadata,
    sqlalchemy.Column("books", sqlalchemy.String)
)

questions = sqlalchemy.Table(
    "questions",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("subject", sqlalchemy.String),
    sqlalchemy.Column("question", sqlalchemy.String),
    sqlalchemy.Column("a", sqlalchemy.String),
    sqlalchemy.Column("b", sqlalchemy.String),
    sqlalchemy.Column("d", sqlalchemy.String),
    sqlalchemy.Column("true", sqlalchemy.String),
    )

rules = sqlalchemy.Table(
    "rules",
    metadata,
    sqlalchemy.Column("one_true_answer", sqlalchemy.FLOAT(1)),
    sqlalchemy.Column("one_false_answer", sqlalchemy.FLOAT(1), nullable=True),
    sqlalchemy.Column("savollar", sqlalchemy.Integer)
)

results = sqlalchemy.Table(
    "results",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("book", sqlalchemy.String),
    sqlalchemy.Column("sovol", sqlalchemy.Integer),
    sqlalchemy.Column("date", sqlalchemy.DateTime),
    sqlalchemy.Column("trues", sqlalchemy.Integer),
    sqlalchemy.Column("falses", sqlalchemy.Integer, nullable=True),
    sqlalchemy.Column("score", sqlalchemy.FLOAT),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger, nullable=True)
)

parent_results = sqlalchemy.Table(
    "parent_results",
    metadata,
    sqlalchemy.Column("id_raqam", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("name", sqlalchemy.String),
    sqlalchemy.Column("surname", sqlalchemy.String),
    sqlalchemy.Column("phone_number", sqlalchemy.String),
    sqlalchemy.Column("username", sqlalchemy.String, nullable=True),
    sqlalchemy.Column("who", sqlalchemy.String),
    sqlalchemy.Column("farzand_sinfi", sqlalchemy.String),
    sqlalchemy.Column("farzand_sinfi_guruxi", sqlalchemy.String),
    sqlalchemy.Column("book", sqlalchemy.String),
    sqlalchemy.Column("score", sqlalchemy.FLOAT),
    sqlalchemy.Column("trues", sqlalchemy.Integer),
    sqlalchemy.Column("falses", sqlalchemy.Integer),
    sqlalchemy.Column("date", sqlalchemy.String, nullable=False),
    sqlalchemy.Column("chat_id", sqlalchemy.BigInteger)
)

students = sqlalchemy.Table(
    "students",
    metadata,
    sqlalchemy.Column("id", sqlalchemy.Integer, primary_key=True),
    sqlalchemy.Column("full_name", sqlalchemy.String),
    sqlalchemy.Column("sinfi", sqlalchemy.String),
    sqlalchemy.Column("guruxi", sqlalchemy.String)
)