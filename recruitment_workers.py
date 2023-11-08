import psycopg2 as pg
from faker import Faker

Faker.seed(12345)
import random

fake = Faker()

conn = pg.connect("dbname=recruitment user=postgres port=5433 password=admin")
cur = conn.cursor()


def generate_worker_account():
    login = fake.pystr_format(string_format='prac_pwr??????', letters='1234567890')
    password = fake.password()
    cur.execute("INSERT INTO accounts (pk_login, password) VALUES (%s, %s)", (login, password))
    return login

workers = []
def generate_worker():
    name = fake.first_name()
    surname = fake.surname()
    phone_number = fake.phone_number()
    mail = fake.email()
    fk_account = generate_worker_account()
    worker_query = "INSERT INTO recruitment_workers (name, surname, phone_number, mail, fk_account) VALUES (%s, %s, %s, %s, %s, %s) RETURNING pk_id"
    cur.execute(
        worker_query,
        (name, surname, phone_number, mail, fk_account))
    workers.append(cur.fetchone()[0])

def generate_worker_for_major():
    major_id_query = "SELECT pk_number FROM majors"
    cur.execute(major_id_query)
    major_id = cur.fetchone()
    for major in major_id:
        workers_for_major_query = "INSERT INTO recruitment_workers_majors (fk_recruitment_worker, fk_major) VALUES (%s, %s)"
        cur.execute(
            workers_for_major_query,
            (workers[random.randint(0, len(workers))], major)
        )


for i in range(40):
    generate_worker()
generate_worker_for_major()
conn.commit()
cur.close()
