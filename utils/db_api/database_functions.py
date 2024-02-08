from main.models import *
from main.database_set import database
from sqlalchemy import and_, text, select
async def get_user(chat_id: int):
    return await database.fetch_one(parents.select().where(parents.c.chat_id==chat_id))

async def get_person(chat_id):
    return await database.fetch_one(query=parents.select().where(parents.c.chat_id==chat_id).with_only_columns(parents.c.farzandi))

async def write_user_table(data: dict):
    return await database.execute(query=parents.insert().values(
        name=data["name"],
        surname=data["surname"],
        phone_number=data["phone_number"],
        username=data["username"],
        farzandi=data["student_name"],
        farzand_sinf=data["classi"],
        farzand_sinf_guruxi=data["bolim"],
        who=data["who"],
        chat_id=data["chat_id"]
    ))

async def insert_class(class_num):
    return await database.execute(query=classes.insert().values(
        class_number=class_num
    ))

async def get_all_classes():
    return await database.fetch_all(query=classes.select().with_only_columns([classes.c.class_number]))

async def insert_new_group(data, new_group):
    return await database.execute(query=groups.insert().values(
        class_number=data["classi"],
        group=new_group
    ))

async def get_all_groups(classi):
    return await database.fetch_all(query=groups.select().where(groups.c.class_number==classi))

async def get_book(book):
    return await database.fetch_one(query=books.select().where(books.c.books==book))

async def insert_admin(chat_id):
    return await database.execute(query=admins.insert().values(
        chat_id=chat_id
    ))

async def update_all():
    return await database.execute(query=rules.insert().values(
        one_true_answer=20.0,
        one_false_answer=20.0,
        savollar=5
    ))

async def delete():
    return await database.execute(query=rules.delete().where(
        rules.c.one_true_answer==20.0,
        rules.c.one_false_answer==20.0,
        rules.c.savollar==5
    ))

async def is_admin(chat_id):
    return await database.fetch_one(admins.select().where(admins.c.chat_id==chat_id))

async def delete_admin(chat_id: int):
    return await database.execute(admins.delete().where(admins.c.chat_id==chat_id))

async def have_class(class_num):
    return await database.fetch_one(classes.select().where(classes.c.class_number==class_num))

async def add_question_to_db(data: dict):
    return await database.execute(questions.insert().values(
        subject=data["book"],
        question=data["question"],
        a=data["a"],
        b=data["b"],
        d=data["d"],
        true=data["true"],
    ))

async def add_new_book(book_name: str):
    return await database.execute(query=books.insert().values(
        books=book_name
    ))



async def get_questions(subject):
    return await database.fetch_all(query=questions.select().where(questions.c.subject==subject))


async def get_sovol1(subject, savol):
    query = questions.select().where(
        questions.c.subject == subject,
        questions.c.question == savol
    ).with_only_columns([questions.c.a, questions.c.b, questions.c.d, questions.c.true])
    result = await database.fetch_one(query=query)
    return result


async def get_questions_security(subject, question):
    query = questions.select().where(
        questions.c.subject == subject,
        questions.c.question.ilike(f"%{question}%")
    )
    return await database.fetch_one(query=query)

async def get_all_book():
    return await database.fetch_all(query=select([books]))

async def get_all_students(sinf, gurux):
    return await database.fetch_all(query=students.select().where(students.c.sinfi==sinf, students.c.guruxi==gurux))

async def get_student(student_name):
    return await database.fetch_one(query=students.select().where(students.c.full_name==student_name).with_only_columns(students.c.full_name))

async def insert_test_user(chat_id, fan, date_time):
    return await database.execute(results.insert().values(
        chat_id=chat_id,
        book=fan,
        score=0,
        sovol=1,
        date=date_time,
        trues=0,
        falses=0
    ))

async def add_student(data: dict):
    return await database.execute(query=students.insert().values(
        full_name=data["full_name"],
        sinfi=data["classi"],
        guruxi=data["class_guruxi"]
    ))

async def delete_user_result(chat_id):
    return await database.execute(query=results.delete().where(results.c.chat_id==chat_id))

async def is_actived(chat_id):
    return await database.fetch_one(query=results.select().where(results.c.chat_id==chat_id))

async def is_true(data: dict, text1):
    return await database.execute(query=questions.select().where(questions.c.subject==data["book"], questions.c.question==data['savol'], questions.c.true==text1))

async def get_true(data: dict):
    return await database.fetch_one(query=questions.select().where(questions.c.question==data['savol'], questions.c.subject==data["book"]).with_only_columns([questions.c.true]))

async def get_achko(chat_id):
    query = results.select().where(results.c.chat_id == chat_id).with_only_columns([results.c.score])
    return await database.fetch_one(query=query)

async def get_all_parent_results(id_nomer: int):
    return await database.fetch_all(query=parent_results.select().where(parent_results.c.id_raqam == id_nomer))


async def get_id_number(id_number):
    return await database.fetch_all(query=parent_results.select().where(parents.c.id_raqam==id_number))

async def get_savol(chat_id):
    query = results.select().where(results.c.chat_id==chat_id).with_only_columns([results.c.sovol])
    return await database.fetch_one(query=query)

async def get_score(chat_id):
    query = results.select().where(results.c.chat_id == chat_id).with_only_columns([results.c.score])
    return await database.fetch_one(query=query)

async def update_user_score(chat_id, scoree, miqdor):
    return await database.execute(
        query=results.update()
        .values(score=scoree + miqdor)
        .where(results.c.chat_id == chat_id)
    )

async def update_user_score_minus(chat_id, scoree, miqdor):
    return await database.execute(
        query=results.update()
        .values(score=scoree - miqdor)
        .where(results.c.chat_id == chat_id)
    )

async def update_user_falses(chat_id, falses):
    return await database.execute(
        query=results.update()
        .values(falses=falses + 1)
        .where(results.c.chat_id == chat_id)
    )

async def update_user_trues(chat_id, trues):
    return await database.execute(
        query=results.update()
        .values(trues=trues + 1)
        .where(results.c.chat_id == chat_id)
    )

async def get_user_trues(chat_id):
    return await database.fetch_one(query=results.select().where(results.c.chat_id==chat_id).with_only_columns([results.c.trues]))

async def get_user_falses(chat_id):
    return await database.fetch_one(query=results.select().where(results.c.chat_id==chat_id).with_only_columns([results.c.falses]))

async def update_user_savol(chat_id, savol):
    return await database.execute(
        query=results.update()
        .values(sovol=savol + 1)
        .where(results.c.chat_id == chat_id)
    )

async def write_results(user, username, result):
    return await database.execute(query=parent_results.insert().values(
        name=str(user["name"]),
        surname=str(user["surname"]),
        phone_number=str(user["phone_number"]),
        username=str(username),
        who=str(user["who"]),
        farzand_sinfi=str(user["farzand_sinf"]),
        farzand_sinfi_guruxi=str(user["farzand_sinf_guruxi"]),
        book=str(result["book"]),
        score=float(result["score"]),
        falses=int(result["falses"]),
        date=str(result["date"]),
        trues=int(result["trues"]),
        chat_id=user["chat_id"]
))

async def update_true_score(new_score: float):
    return await database.execute(query=rules.update().values(
        one_true_answer=new_score
    ))

async def update_false_score(new_score: float):
    return await database.execute(query=rules.update().values(
        one_false_answer=new_score
    ))

async def update_miqdor(new_score: int):
    return await database.execute(query=rules.update().values(
        savollar=new_score
    ))

async def chegara():
    return await database.fetch_all(query=select(rules))

async def insert_chegara():
    return await database.execute(query=rules.insert().values(
        one_true_answer=20.5,
        one_false_answer=15.5,
        savollar=5
    ))

async def get_all_admins():
    return await database.fetch_all(query=select([admins]))

async def get_user_result(chat_id):
    return await database.fetch_one(query=results.select().where(results.c.chat_id==chat_id))

async def delete_admin(chat_id):
    return await database.execute(query=admins.delete().where(admins.c.chat_id==chat_id))

async def delete_books(book_name):
    await database.execute(query=books.delete().where(books.c.books == book_name))
    await database.execute(query=questions.delete().where(questions.c.subject == book_name))