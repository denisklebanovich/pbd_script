import random
import psycopg2 as pg
from faker import Faker
from random_pesel import RandomPESEL

fake = Faker()

# TODO: recruitment_exemption_document_types
# TODO: document_exempting_from_fees_types

# Connect to an existing database
conn = pg.connect("dbname=recruitment user=postgres port=5433 password=admin")
cur = conn.cursor()

# THRESHOLDS
thresholds_data = [
    (random.randint(1, 10), random.randint(1, 10)) for _ in range(10)
]

cur.execute("INSERT INTO id_document_types (pk_name) VALUES (%s)", ("passport",))
cur.execute("INSERT INTO id_document_types (pk_name) VALUES (%s)", ("id_card",))

cur.execute("INSERT INTO recruitment_exemption_document_types (pk_name) VALUES (%s)", ("disability_certificate",))
cur.execute("INSERT INTO recruitment_exemption_document_types (pk_name) VALUES (%s)", ("certificate_of_completion_of_the_first_degree",))
cur.execute("INSERT INTO recruitment_exemption_document_types (pk_name) VALUES (%s)", ("certificate_of_completion_of_the_second_degree",))
cur.execute("INSERT INTO recruitment_exemption_document_types (pk_name) VALUES (%s)", ("certificate_of_completion_of_the_third_degree",))
cur.execute("INSERT INTO recruitment_exemption_document_types (pk_name) VALUES (%s)", ("certificate_of_completion_of_the_first_degree_of_music_school",))
cur.execute("INSERT INTO recruitment_exemption_document_types (pk_name) VALUES (%s)", ("certificate_of_completion_of_the_first_degree_of_art_school",))

cur.execute("INSERT INTO document_exempting_from_fees_types (pk_name) VALUES (%s)", ("disability_certificate",))
cur.execute("INSERT INTO document_exempting_from_fees_types (pk_name) VALUES (%s)", ("certificate_of_completion_of_the_first_degree",))
cur.execute("INSERT INTO document_exempting_from_fees_types (pk_name) VALUES (%s)", ("certificate_of_completion_of_the_second_degree",))


# DEPARTMENT
departments = {
    "Architecture": "Department of Architecture is focused on architectural design and theory.",
    "Civil Engineering": "The Department of Civil Engineering specializes in infrastructure and construction projects.",
    "Chemistry": "The Chemistry Department offers a wide range of courses in chemical science.",
    "Electronics": "The Electronics Department focuses on electronic systems and devices.",
    "Electrical Engineering": "Department of Electrical Engineering offers programs in electrical systems.",
    "Microsystem Electronics and Photonics": "This department specializes in microelectronics and photonics.",
    "Computer Science and Management": "Department of Computer Science and Management covers computer-related fields.",
    "Geodesy and Geoinformatics": "This department is involved in geospatial science and information technology.",
    "Environmental Engineering": "Environmental Engineering Department deals with environmental issues and solutions.",
    "Fundamental Problems of Technology": "This department focuses on fundamental technological research.",
    "Pure and Applied Mathematics": "The Department of Mathematics offers courses in pure and applied math.",
    "Mechanical Engineering": "Department of Mechanical Engineering focuses on mechanical systems.",
    "Machines and Transport": "This department deals with machines and transportation technologies.",
    "Materials Engineering": "The Materials Engineering Department specializes in materials science.",
    "Mechanical and Power Engineering": "This department focuses on mechanical and power systems.",
    "Technology and Engineering": "Technology and Engineering Department covers various engineering fields.",
    "Applied Informatics": "Department of Applied Informatics deals with practical computer science.",
    "Organization and Management": "This department is involved in the study of organizations and management.",
}

# MAJORS
majors_by_department = {
    "Architecture": [
        {"name": "Architecture", "description": "Designing buildings and structures"},
        {"name": "Urban Planning", "description": "Planning urban spaces"},
        {"name": "Interior Design", "description": "Designing interior spaces"},
    ],
    "Civil Engineering": [
        {"name": "Civil Engineering", "description": "Designing and constructing civil structures"},
        {"name": "Structural Engineering", "description": "Analyzing and designing structures"},
    ],
    "Chemistry": [
        {"name": "Chemistry", "description": "Study of chemical elements and compounds"},
        {"name": "Biochemistry", "description": "Study of chemical processes within living organisms"},
    ],
    "Electronics": [
        {"name": "Electronics", "description": "Study of electronic components and circuits"},
        {"name": "Digital Systems", "description": "Design and analysis of digital systems"},
    ],
    "Electrical Engineering": [
        {"name": "Electrical Engineering", "description": "Study of electrical systems and devices"},
        {"name": "Power Systems", "description": "Design and analysis of power systems"},
        {"name": "Control Systems", "description": "Study of control engineering"},
    ],
    "Microsystem Electronics and Photonics": [
        {"name": "Microsystem Electronics", "description": "Study of microelectronic devices"},
        {"name": "Photonics", "description": "Study of the generation and manipulation of light"},
    ],
    "Computer Science and Management": [
        {"name": "Computer Science", "description": "Study of algorithms and programming"},
        {"name": "Information Systems", "description": "Design and management of information systems"},
        {"name": "Management", "description": "Study of organizational management principles"},
        {"name": "Cybersecurity", "description": "Study of securing computer systems and networks"},
    ],
    "Geodesy and Geoinformatics": [
        {"name": "Geodesy", "description": "Study of Earth's geometry and physical properties"},
        {"name": "Geoinformatics", "description": "Application of information science to spatial data"},
    ],
    "Environmental Engineering": [
        {"name": "Environmental Engineering", "description": "Environmental impact assessment"},
        {"name": "Ecological Engineering", "description": "Study of ecological systems and environmental protection"},
    ],
    "Fundamental Problems of Technology": [
        {"name": "Materials Science", "description": "Study of materials and their properties"},
        {"name": "Nanotechnology",
         "description": "Study of manipulation of matter on an atomic, molecular, and supramolecular scale"},
        {"name": "Biotechnology", "description": "Application of biological systems for technological advancements"},
    ],
    "Pure and Applied Mathematics": [
        {"name": "Pure Mathematics", "description": "Study of abstract structures and relationships"},
        {"name": "Applied Mathematics",
         "description": "Application of mathematical methods to solve real-world problems"},
    ],
    "Mechanical Engineering": [
        {"name": "Mechanical Engineering", "description": "Design and analysis of mechanical systems"},
        {"name": "Mechatronics",
         "description": "Integration of mechanical engineering with electronics and computer science"},
        {"name": "Automotive Engineering", "description": "Design and production of automotive systems"},
    ],
    "Machines and Transport": [
        {"name": "Machine Construction", "description": "Design and manufacturing of machines"},
        {"name": "Transportation Engineering", "description": "Study of transportation systems and infrastructure"},
    ],
    "Materials Engineering": [
        {"name": "Materials Engineering", "description": "Study of materials and their properties"},
        {"name": "Metallurgy", "description": "Study of metals and alloys"},
        {"name": "Ceramic Engineering", "description": "Study of ceramic materials and their applications"},
    ],
    "Mechanical and Power Engineering": [
        {"name": "Power Engineering", "description": "Study of energy production and utilization"},
        {"name": "Renewable Energy", "description": "Study of sustainable energy sources"},
        {"name": "Fluid Mechanics", "description": "Study of fluid behavior"},
    ],
    "Technology and Engineering": [
        {"name": "Engineering Technology", "description": "Application of engineering principles to technology"},
        {"name": "Robotics", "description": "Study of designing and building robots"},
    ],
    "Applied Informatics": [
        {"name": "Applied Informatics",
         "description": "Application of information technology to solve practical problems"},
        {"name": "Data Science", "description": "Study of extracting insights and information from data"},
    ],
    "Organization and Management": [
        {"name": "Organization and Management", "description": "Study of organizational management principles"},
        {"name": "Project Management", "description": "Planning and executing projects efficiently"},
        {"name": "Human Resource Management", "description": "Study of managing human resources in organizations"},
    ]
}


# MAJOR ALGORITHMS
algorithms = ["Algorithm for IT majors", "Algorithm for non-IT majors", "Algorithm for geodesy majors"]
algorithms_query = "INSERT INTO major_algorithms (pk_name) VALUES (%s)"
cur.executemany(algorithms_query, [(algorithm,) for algorithm in algorithms])


cur.execute("SELECT pk_name FROM major_algorithms")
MAJOR_ALGORITHMS = cur.fetchall()
# Generate data for the "departments" table
departments_data = [(name, description) for name, description in departments.items()]
departments_query = "INSERT INTO departments (name, description) VALUES (%s, %s) RETURNING pk_number, name"
for department in departments_data:
    cur.execute(departments_query, department)
    department_id, department_name = cur.fetchone()
    majors = majors_by_department[department_name]
    majors_data = [(major["name"], major["description"], random.randint(50, 180), department_id,random.choice(MAJOR_ALGORITHMS)) for major in majors]
    majors_query = "INSERT INTO majors (nazwa, description, number_of_places, fk_department,fk_algorithm) VALUES (%s, %s, %s, %s, %s)"
    cur.executemany(majors_query, majors_data)

# EXAM TYPES
exam_types = {
    "Old Matura": {
        "minimum_score": 1.0,
        "maximum_score": 6.0,
        "multiplier": 16.666,
    },
    "New Matura": {
        "minimum_score": 0,
        "maximum_score": 100,
        "multiplier": 1,
    },
    "University Exam": {
        "minimum_score": 0,
        "maximum_score": 100,
        "multiplier": 1,
    }
}

# Generate data for the "exam_types" table
exam_types_data = []
for name, data in exam_types.items():
    exam_types_data.append((name, data["minimum_score"], data["maximum_score"], data["multiplier"]))
exam_types_query = "INSERT INTO exam_types (pk_name, minimum_points_score, maximum_points_score, multiplier) VALUES (%s, %s, %s, %s)"
cur.executemany(exam_types_query, exam_types_data)

cur.execute("SELECT pk_id FROM majors")
MAJORS = cur.fetchall()

# Thresholds
def generate_thresholds():
    thresholds_data = {}
    for major_id in MAJORS:
        for year in range(2018, 2023):
            previous_year_thresholds = [(major_id, year)] if (major_id, year) in thresholds_data else round(random.uniform(20, 500), 1)
            first_round = min(max(previous_year_thresholds+round(random.uniform(-50, 50), 1), 20.0), 500.0)
            second_round = min(max(first_round+round(random.uniform(-50, 50), 1), 20.0), 500.0)
            third_round = min(max(second_round+round(random.uniform(-50, 50), 1), 20.0), 500.0)
            thresholds_data.update({
                (major_id, year) : {
                                    "round_1": first_round,
                                    "round_2": second_round,
                                    "round_3": third_round}
            })
    return thresholds_data

thresholds = generate_thresholds()
for key, value in thresholds.items():
    major_id, year = key
    add_thresholds_query = "INSERT INTO thresholds (fk_major, recrutation_year, round_1, round_2, round_3) VALUES (%s, %s, %s, %s, %s)"
    cur.execute(add_thresholds_query, (major_id, year, value["round_1"], value["round_2"], value["round_3"]))

# COURSE
majors_with_courses = {
    'Architecture': [
        {'Architecture': 'Designing buildings and structures'},
        {'Urban Planning': 'Planning urban spaces'},
        {'Interior Design': 'Designing interior spaces'},
    ],
    'Civil Engineering': [
        {'Civil Engineering': 'Designing and constructing civil structures'},
        {'Structural Engineering': 'Analyzing and designing structures'},
    ],
    'Chemistry': [
        {'Chemistry': 'Study of chemical elements and compounds'},
        {'Biochemistry': 'Study of chemical processes within living organisms'},
    ],
    'Electronics': [
        {'Electronics': 'Study of electronic components and circuits'},
        {'Digital Systems': 'Design and analysis of digital systems'},
    ],
    'Electrical Engineering': [
        {'Electrical Engineering': 'Study of electrical systems and devices'},
        {'Power Systems': 'Design and analysis of power systems'},
        {'Control Systems': 'Study of control engineering'},
    ],
    'Microsystem Electronics': [
        {'Microsystem Electronics': 'Study of microelectronic devices'},
        {'Photonics': 'Study of the generation and manipulation of light'},
    ],
    'Computer Science': [
        {'Computer Science': 'Study of algorithms and programming'},
        {'Information Systems': 'Design and management of information systems'},
        {'Management': 'Study of organizational management principles'},
        {'Cybersecurity': 'Study of securing computer systems and networks'},
    ],
    'Geodesy': [
        {'Geodesy': 'Study of Earth\'s geometry and physical properties'},
        {'Geoinformatics': 'Application of information science to spatial data'},
    ],
    'Environmental Engineering': [
        {'Environmental Engineering': 'Environmental impact assessment'},
        {'Ecological Engineering': 'Study of ecological systems and environmental protection'},
    ],
    'Materials Science': [
        {'Materials Science': 'Study of materials and their properties'},
        {'Nanotechnology': 'Study of manipulation of matter on an atomic, molecular, and supramolecular scale'},
        {'Biotechnology': 'Application of biological systems for technological advancements'},
    ],
    'Pure Mathematics': [
        {'Pure Mathematics': 'Study of abstract structures and relationships'},
        {'Applied Mathematics': 'Application of mathematical methods to solve real-world problems'},
    ],
    'Mechanical Engineering': [
        {'Mechanical Engineering': 'Design and analysis of mechanical systems'},
        {'Mechatronics': 'Integration of mechanical engineering with electronics and computer science'},
        {'Automotive Engineering': 'Design and production of automotive systems'},
    ],
    'Machine Construction': [
        {'Machine Construction': 'Design and manufacturing of machines'},
        {'Transportation Engineering': 'Study of transportation systems and infrastructure'},
    ],
    'Materials Engineering': [
        {'Materials Engineering': 'Study of materials and their properties'},
        {'Metallurgy': 'Study of metals and alloys'},
        {'Ceramic Engineering': 'Study of ceramic materials and their applications'},
    ],
    'Renewable Energy': [
        {'Power Engineering': 'Study of energy production and utilization'},
        {'Renewable Energy': 'Study of sustainable energy sources'},
        {'Fluid Mechanics': 'Study of fluid behavior'},
    ],
    'Robotics': [
        {'Engineering Technology': 'Application of engineering principles to technology'},
        {'Robotics': 'Study of designing and building robots'},
    ],
    'Applied Informatics': [
        {'Applied Informatics': 'Application of information technology to solve practical problems'},
        {'Data Science': 'Study of extracting insights and information from data'},
    ],
    'Organization and Management': [
        {'Organization and Management': 'Study of organizational management principles'},
        {'Project Management': 'Planning and executing projects efficiently'},
        {'Human Resource Management': 'Study of managing human resources in organizations'},
    ],
}

def set_courses():
    for major_name, courses in majors_with_courses.items():
        major_id_query = "SELECT pk_id FROM majors WHERE nazwa = %s"
        cur.execute(major_id_query, (major_name,))
        major_id = cur.fetchone()[0]
        if not major_id:
            continue
        for course in courses:
            course_name = list(course.keys())[0]
            course_description = list(course.values())[0]
            course_query = "INSERT INTO courses (name, description, fk_major) VALUES (%s, %s, %s)"
            cur.execute(course_query, (course_name, course_description, major_id))

set_courses()

# NATIONALITIES
european_nationalities = [
    {"name": "Albanian", "studies_fee_free": False},
    {"name": "Austrian", "studies_fee_free": True},
    {"name": "Belgian", "studies_fee_free": True},
    {"name": "Belarusian","studies_fee_free": False},
    {"name": "Bosnian", "studies_fee_free": False},
    {"name": "Bulgarian", "studies_fee_free": True},
    {"name": "Croatian", "studies_fee_free": True},
    {"name": "Czech", "studies_fee_free": True},
    {"name": "Danish", "studies_fee_free": True},
    {"name": "Estonian", "studies_fee_free": True},
    {"name": "Finnish", "studies_fee_free": True},
    {"name": "Greek", "studies_fee_free": True},
    {"name": "Hungarian", "studies_fee_free": True},
    {"name": "Icelandic", "studies_fee_free": True},
    {"name": "Irish", "studies_fee_free": True},
    {"name": "Italian", "studies_fee_free": True},
    {"name": "Latvian", "studies_fee_free": True},
    {"name": "Lithuanian", "studies_fee_free": True},
    {"name": "Luxembourgish", "studies_fee_free": True},
    {"name": "Maltese", "studies_fee_free": True},
    {"name": "Moldovan", "studies_fee_free": False},
    {"name": "Monégasque", "studies_fee_free": True},
    {"name": "Montenegrin", "studies_fee_free": False},
    {"name": "Dutch", "studies_fee_free": True},
    {"name": "Norwegian", "studies_fee_free": True},
    {"name": "Polish", "studies_fee_free": True},
    {"name": "Portuguese", "studies_fee_free": True},
    {"name": "Romanian", "studies_fee_free": True},
    {"name": "Russian", "studies_fee_free": False},
    {"name": "Serbian", "studies_fee_free": False},
    {"name": "Slovak", "studies_fee_free": True},
    {"name": "Slovenian", "studies_fee_free": True},
    {"name": "Spanish", "studies_fee_free": True},
    {"name": "Swedish", "studies_fee_free": True},
    {"name": "Swiss", "studies_fee_free": True},
    {"name": "Turkish", "studies_fee_free": False},
    {"name": "Ukrainian", "studies_fee_free": False},
    {"name": "British", "studies_fee_free": True},
    {"name": "Uzbek", "studies_fee_free": False},
    {"name": "Kazakh", "studies_fee_free": False},
    {"name": "Canadian", "studies_fee_free": False},
    {"name": "Australian", "studies_fee_free": False},
    {"name": "Japanese", "studies_fee_free": False},
]

nationalities_data = []
for nationality in european_nationalities:
    nationalities_data.append((nationality["name"], nationality["studies_fee_free"]))
nationalities_query = "INSERT INTO nationalities (pk_name, studies_fee_free) VALUES (%s, %s)"
cur.executemany(nationalities_query, nationalities_data)


# CANDIDATE
def choose_nationality():
    polish_vs_european = [european_nationalities, [{"name": "Polish"}]]
    return random.choice(random.choices(population=polish_vs_european,
                            weights=[0.2, 0.8]))["name"]



# SUBJECTS
subject_names = [
    "Mathematics",
    "Physics",
    "Computer Science",
    "Biology",
    "Chemistry",
    "History",
    "Literature",
    "Art",
    "Economics",
    "Geography"
]

subjects_data = [(name,) for name in subject_names]
subjects_query = "INSERT INTO subjects (pk_name) VALUES (%s)"
cur.executemany(subjects_query, subjects_data)

# SUBJECTS MENTIONED IN ALGORITHM
subjects_mentioned_in_algorithm = [
    {
        "fk_subject": "Mathematics",
        "fk_algorithm": "Algorithm for IT majors",
        "factor": 2.5
    },
    {
        "fk_subject": "Computer Science",
        "fk_algorithm": "Algorithm for IT majors",
        "factor": 2.5
    },
    {
        "fk_subject": "Physics",
        "fk_algorithm": "Algorithm for IT majors",
        "factor": 2.5
    },
    {
        "fk_subject": "Mathematics",
        "fk_algorithm": "Algorithm for non-IT majors",
        "factor": 2.5
    },
    {
        "fk_subject": "Physics",
        "fk_algorithm": "Algorithm for non-IT majors",
        "factor": 2.5
    },
    {
        "fk_subject": "Literature",
        "fk_algorithm": "Algorithm for non-IT majors",
        "factor": 0.1
    },
    {
        "fk_subject": "Literature",
        "fk_algorithm": "Algorithm for IT majors",
        "factor": 0.1
    },
    {
        "fk_subject": "Literature",
        "fk_algorithm": "Algorithm for geodesy majors",
        "factor": 0.1
    },
    {
        "fk_subject": "Geography",
        "fk_algorithm": "Algorithm for geodesy majors",
        "factor": 2.5
    },
    {
        "fk_subject": "Mathematics",
        "fk_algorithm": "Algorithm for geodesy majors",
        "factor": 2.5
    },
    {
        "fk_subject": "Physics",
        "fk_algorithm": "Algorithm for IT majors",
        "factor": 2.5
    }
]

subjects_mentioned_in_algorithm_data = []
for subject in subjects_mentioned_in_algorithm:
    subjects_mentioned_in_algorithm_data.append((subject["fk_subject"], subject["fk_algorithm"], subject["factor"]))
subjects_mentioned_in_algorithm_query = "INSERT INTO subjects_mentioned_in_algorithm (fk_subject, fk_algorithm, factor) VALUES (%s, %s, %s)"
cur.executemany(subjects_mentioned_in_algorithm_query, subjects_mentioned_in_algorithm_data)


fake = Faker()
fake_pesel = RandomPESEL()

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
    login = fake.unique.pystr_format(string_format='pwr??????', letters='1234567890')
    cur.execute("SELECT * FROM accounts WHERE pk_login = %s", (login,))
    password = fake.password()
    cur.execute("INSERT INTO accounts (pk_login, password) VALUES (%s, %s)", (login, password))
    return login


def get_document_type_with_nationality():
    is_polish = random.choices([True, False], weights=[0.9, 0.1])[0]
    if is_polish:
        return "id_card", "Polish"
    else:
        return "passport", random.choice(NATIONALITIES)

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
    avg_mark = round(random.uniform(3.0, 5.0), 3)
    thesis_mark = random.choices([3.0, 3.5, 4.0, 4.5, 5.0], weights=[0.1, 0.2, 0.3, 0.2, 0.15])[0]
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

    generate_recruitment_applications(candidate_id)

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


# RECRUITMENT_APPLICATIONS
def generate_recruitment_applications(candidate_id):
    numbers_of_applications = random.randint(1, 5)
    for i in range(numbers_of_applications):
        year = random.choice([2017,2018,2019, 2020, 2021,2022,2023])
        round = random.choice(["FIRST", "SECOND", "THIRD"])
        major = random.choice(MAJORS)
        cur.execute("INSERT INTO recruitment_applications (fk_major, fk_candidate, year,round) VALUES (%s, %s, %s, %s)",
                    (major, candidate_id, year, round))


def generate_worker_account():
    login = fake.unique.pystr_format(string_format='prac_pwr??????', letters='1234567890')
    password = fake.password()
    cur.execute("INSERT INTO accounts (pk_login, password) VALUES (%s, %s)", (login, password))
    return login

workers = []
def generate_worker():
    name = fake.first_name()
    surname = fake.last_name()
    phone_number = fake.phone_number()
    mail = fake.email()
    fk_account = generate_worker_account()
    worker_query = "INSERT INTO recruitment_workers (name, surname, phone_number, mail, fk_account) VALUES (%s, %s, %s, %s, %s) RETURNING pk_id"
    cur.execute(
        worker_query,
        (name, surname, phone_number, mail, fk_account))
    workers.append(cur.fetchone()[0])

def generate_worker_for_major():
    for major in MAJORS:
        worker_number = random.randint(1, 5)
        workers_for_major = random.choices(workers, k=worker_number)
        for worker in workers_for_major:
            cur.execute("INSERT INTO recruitment_workers_majors (fk_recruitment_worker, fk_major) VALUES (%s, %s)",
                        (worker, major[0]))


for i in range(200):
    generate_worker()

generate_worker_for_major()

for i in range(20000):
    generate_candidate()




conn.commit()
cur.close()
conn.close()