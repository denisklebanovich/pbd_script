import psycopg2 as pg
from faker import Faker
from random_pesel import RandomPESEL
import random

fake = Faker()
fake_pesel = RandomPESEL()

conn = pg.connect("dbname=recruitment user=postgres port=5433 password=admin")
cur = conn.cursor()

# CONSTS
cur.execute("SELECT pk_name FROM nationalities")
NATIONALITIES = cur.fetchall()

cur.execute("SELECT pk_name FROM exam_types")
EXAM_TYPES = cur.fetchall()

cur.execute("SELECT pk_name FROM subjects")
SUBJECTS = cur.fetchall()

cur.execute("SELECT pk_name FROM recruitment_exemption_document_types")
RECRUITMENT_EXEMPTION_DOCUMENT_TYPES = cur.fetchall()

cur.execute("SELECT pk_name FROM document_exempting_from_fees_types")
DOCUMENT_EXEMPTING_FROM_FEES_TYPES = cur.fetchall()


universities = [
    "University of Warsaw",
    "Jagiellonian University",
    "Warsaw University of Technology",
    "Adam Mickiewicz University in Poznań",
    "AGH University of Science and Technology",
    "Wrocław University of Science and Technology",
    "University of Wrocław",
    "Gdańsk University of Technology",
    "University of Gdańsk",
    "Silesian University of Technology",
    "Nicolaus Copernicus University in Toruń",
    "Poznań University of Technology",
    "University of Łódź",
    "Warsaw School of Economics",
    "Medical University of Warsaw",
    "University of Silesia in Katowice",
    "Poznań University of Life Sciences",
    "Wrocław University of Environmental and Life Sciences",
    "Lublin University of Technology",
    "Cracow University of Economics",
    "Warsaw University of Life Sciences",
    "University of Warmia and Mazury in Olsztyn",
    "Kazimierz Wielki University in Bydgoszcz",
    "University of Rzeszów",
    "Częstochowa University of Technology",
    "Pomeranian Medical University in Szczecin",
    "University of Zielona Góra",
    "Opole University of Technology",
    "Cardinal Stefan Wyszyński University in Warsaw",
    "University of Opole",
    "Poznań University of Economics and Business",
    "Jan Kochanowski University in Kielce",
    "Kielce University of Technology",
    "University of Information Technology and Management in Rzeszów",
    "Maria Curie-Skłodowska University in Lublin",
    "Bialystok University of Technology",
    "University of Bielsko-Biała",
    "Nicolaus Copernicus University Collegium Medicum in Bydgoszcz",
    "University of Agriculture in Krakow",
    "University of Social Sciences and Humanities in Warsaw",
    "Lodz University of Technology",
    "Lomza State University of Applied Sciences",
    "Warsaw University of Social Sciences and Humanities",
    "Warsaw Medical University",
    "University of Lower Silesia in Wrocław",
    "WSB University in Wrocław",
    "MIT",
    "Stanford University",
    "Harvard University",
    "University of Oxford",
    "University of Cambridge",
    "California Institute of Technology",
    "ETH Zurich",
    "University of Chicago",
]

def generate_candidate_account():
    login = fake.pystr_format(string_format='pwr??????', letters='1234567890')
    password = fake.password()
    cur.execute("INSERT INTO accounts (pk_login, password) VALUES (%s, %s)", (login, password))
    return login


def get_document_type_with_nationality():
    is_polish = random.choices([True, False], weights=[0.9, 0.1])[0]
    if is_polish:
        return 1, "Polish"
    else:
        return 2, random.choice(NATIONALITIES)

def generate_exam_results(candidate_id):
    document_id = fake.pystr(min_chars=6, max_chars=20)
    date = fake.date_between(start_date='-5y', end_date='today')
    exam_type = random.choice(EXAM_TYPES)
    cur.execute("INSERT INTO exams (document_id, fk_candidate, date, fk_exam_type) VALUES (%s, %s, %s, %s) RETURNING pk_id",
                (document_id, candidate_id, date, exam_type))
    exam_id = cur.fetchone()[0]
    generate_subject_results(exam_id)

def generate_subject_results(exam_id):
    subject_len = random.randint(1, 5)
    subjects = random.choices(SUBJECTS, k=subject_len)
    for subject in subjects:
        points = random.randint(0, 100)
        cur.execute("INSERT INTO subject_results (fk_subject, fk_exam, points) VALUES (%s, %s, %s)",
                    (subject, exam_id, points))


def generate_dyploma(candidate_id):
    university = random.choice(universities)
    avg_mark = round(random.uniform(2.0, 5.0), 3)
    thesis_mark = random.choices([2.0, 3.0, 3.5, 4.0, 4.5, 5.0], weights=[0.05, 0.1, 0.2, 0.3, 0.2, 0.15])[0]
    cur.execute("INSERT INTO first_degree_diplomas (fk_candidate, university_name, average_mark, thesis_mark) VALUES (%s, %s, %s, %s)",
                (candidate_id, university, avg_mark, thesis_mark))

def generate_recrutation_exemption_document(candidate_id):
    document_type = random.choice(RECRUITMENT_EXEMPTION_DOCUMENT_TYPES)
    cur.execute("INSERT INTO recruitment_exemption_documents (fk_candidate, fk_type) VALUES (%s, %s)",
                (candidate_id, document_type))

def generate_fee_exempting_document(candidate_id):
    document_type = random.choice(DOCUMENT_EXEMPTING_FROM_FEES_TYPES)
    date_of_issue = fake.date_between(start_date='-2y', end_date='today')
    document_id = fake.pystr(min_chars=6, max_chars=20)
    cur.execute("INSERT INTO documents_exempting_from_fees (fk_type, fk_candidate, date_of_issue, document_id) VALUES (%s, %s, %s, %s)",
                (document_type, candidate_id, date_of_issue, document_id))




def generate_candidate():
    account_id = generate_candidate_account()
    name = fake.first_name()
    surname = fake.last_name()
    id_document_number = fake.passport_number()
    document_type_id, nationality = get_document_type_with_nationality()
    pesel = None
    if nationality == "Polish":
        pesel = fake_pesel.generate()
    cur.execute("INSERT INTO candidates (fk_account, name, surname, id_document_number, fk_id_document_type,fk_nationality, pesel) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING pk_id",
                (account_id, name, surname, id_document_number, document_type_id, nationality, pesel))
    candidate_id = cur.fetchone()[0]
    if nationality != "Polish":
        has_document_exempting_from_fees = random.choices([True, False], weights=[0.05, 0.95])[0]
        if has_document_exempting_from_fees:
            generate_fee_exempting_document(candidate_id)
    is_bachelor = random.choices([True, False], weights=[0.8, 0.2])[0]
    if is_bachelor:
        has_exam_results = random.choices([True, False], weights=[0.95, 0.05])[0]
        if has_exam_results:
            generate_exam_results(candidate_id)
    else:
        has_dyploma = random.choices([True, False], weights=[0.95, 0.05])[0]
        if has_dyploma:
            generate_dyploma(candidate_id)

    has_recruitment_exemption_document = random.choices([True, False], weights=[0.02, 0.98])[0]

    if has_recruitment_exemption_document:
        generate_recrutation_exemption_document(candidate_id)

cur.execute("SELECT pk_id FROM majors")
MAJORS = cur.fetchall()

# RECRUITMENT_APPLICATIONS
def generate_recruitment_applications(candidate_id):
    numbers_of_applications = random.randint(1, 5)
    for i in range(numbers_of_applications):
        year = random.choice([2017,2018,2019, 2020, 2021,2022,2023])
        round = random.choice(["FIRST", "SECOND", "THIRD"])
        major = random.choice(MAJORS)
        cur.execute("INSERT INTO recruitment_applications (fk_major, fk_candidate, year,round) VALUES (%s, %s, %s, %s)",
                    (major, candidate_id, year, round))


conn.commit()
cur.close()
