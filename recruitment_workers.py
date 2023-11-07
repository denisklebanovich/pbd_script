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


def generate_worker():
    name = fake.first_name()
    surname = fake.surname()
    phone_number = fake.phone_number()
    mail = fake.email()
    fk_account = generate_worker_account()
    worker_query = "INSERT INTO recruitment_workers ()"

generate_worker()
conn.commit()
cur.close()
