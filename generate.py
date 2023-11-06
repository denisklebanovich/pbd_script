import random
import string

import psycopg2 as pg
from faker import Faker
from random_pesel import RandomPESEL
import random_pesel

fake = Faker()

# Connect to an existing database
conn = pg.connect("dbname=recruitment user=postgres port=5433 password=admin")
cur = conn.cursor()

# 1st DEGREE DYPLOMAS
polish_universities = [
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
]
# Generate data for the "1st_degree_diplomas" table
diplomas_data = [
    (
        random.choice(polish_universities),  # University name
        round(random.uniform(3.0, 4.0), 3),  # Average mark (between 3.0 and 4.0)
        random.choice([3, 3.5, 4.0, 4.5, 5.0]),  # Thesis mark (between 3.0 and 5.0)
        random.randint(1, 10),  # fk_candidate (adjust the range based on the number of candidates)
    )
    for _ in range(10)  # Adjust the number of diplomas as needed
]

# THRESHOLDS
thresholds_data = [
    (random.randint(1, 10), random.randint(1, 10)) for _ in range(10)
]

# SURNAMES
surnames = [
    "Nowak",
    "Kowalski",
    "Wiśniewski",
    "Wójcik",
    "Kowalczyk",
    "Kamiński",
    "Lewandowski",
    "Zieliński",
    "Szymański",
    "Woźniak",
    "Dąbrowski",
    "Kozłowski",
    "Jankowski",
    "Mazur",
    "Wojciechowski",
    "Kwiatkowski",
    "Kaczmarek",
    "Piotrowski",
    "Grabowski",
    "Zając",
    "Krawczyk",
    "Pawłowski",
    "Michalski",
    "Król",
    "Wieczorek",
    "Jabłoński",
    "Wróbel",
    "Dudek",
    "Adamczyk",
    "Olszewski",
    "Jaworski",
    "Malinowski",
    "Pawlak",
    "Górski",
    "Sikora",
    "Walczak",
    "Rutkowski",
    "Baran",
    "Michalak",
    "Szewczyk",
    "Ostrowski",
    "Tomaszewski",
    "Pietrzak",
    "Marciniak",
    "Wróblewski",
    "Zalewski",
    "Jakubowski",
    "Jasiński",
    "Zawisza",
    "Sadowski",
    "Błaszczyk",
    "Sawicki",
    "Kubiak",
    "Lis",
    "Kołodziej",
    "Urbaniak",
    "Maciejewski",
    "Kielbasa",
    "Gajos",
    "Sobolewski",
    "Wesołowski",
    "Kalinowski",
    "Konieczny",
    "Wilczak",
    "Zieliński",
    "Kołodziej",
    "Głowacki",
    "Ławniczak",
    "Szczepański",
    "Kaczmarek",
    "Gajda",
    "Sobczak",
    "Kozak",
    "Kurowski",
    "Baranowski",
    "Majewski",
    "Czarnecki",
    "Rogalski",
    "Oleksy",
    "Kurek",
    "Nawrocki",
    "Leszczynski",
    "Stanisławski",
    "Kolasa",
    "Koper",
    "Dzięgiel",
    "Karcz",
    "Biernacki",
    "Gomółka",
    "Niedźwiecki",
    "Kubacki",
    "Budny",
    "Serafin",
    "Szostak",
    "Wawrzyniak",
    "Korzeniowski",
    "Kopacz",
    "Pawlik",
    "Krzesiński",
    "Markiewicz",
    "Szymczak",
    "Jabłoński",
    "Malczewski",
    "Olszak",
    "Wright",
    "Adams",
    "Allen",
    "Carter",
    "Davis",
    "Garcia",
    "Gray",
    "Johnson",
    "Jones",
    "Kelly",
    "King",
    "Martinez",
    "Nelson",
    "Phillips",
    "Roberts",
    "Scott",
    "Taylor",
    "Thomas",
    "Thompson",
    "Williams",
    "Wilson",
    "Young",
    "Allen",
    "Baker",
    "Brown",
    "Carter",
    "Clark",
    "Cook",
    "Davis",
]

# NAMES
names = [
    "Aleksandra",
    "Andrzej",
    "Barbara",
    "Bartosz",
    "Beata",
    "Czesław",
    "Dorota",
    "Dariusz",
    "Elżbieta",
    "Filip",
    "Grażyna",
    "Grzegorz",
    "Hanna",
    "Jacek",
    "Joanna",
    "Jan",
    "Katarzyna",
    "Krzysztof",
    "Magdalena",
    "Marek",
    "Małgorzata",
    "Michał",
    "Monika",
    "Paweł",
    "Renata",
    "Robert",
    "Teresa",
    "Tomasz",
    "Wanda",
    "Wojciech",
    "Zofia",
    "Łukasz",
    "Łucja",
    "Wioletta",
    "Zbigniew",
    "Świętosław",
    "Władysław",
    "Krystyna",
    "Stanisław",
    "Agnieszka",
    "Rafał",
    "Ewa",
    "Mariusz",
    "Kinga",
    "Radosław",
    "Sylwia",
    "Maciej",
    "Justyna",
]


def generate_student_login(prefix='pwr'):
    generate_student_login.num += 1
    return prefix + str(generate_student_login.num)


generate_student_login.num = 10000


def generate_worker_login(prefix='pwr_prac'):
    generate_worker_login.num += 1
    return prefix + str(generate_worker_login.num)


generate_worker_login.num = 100

# PASSWORDS
passwords = [
    "123456", "qwerty", "123456789", "12345", "zaq12wsx", "password", "12345678", "polska",
    "1234567", "123qwe", "1234567890", "misiek", "lol123", "mateusz", "marcin", "qwe123",
    "monika", "qwerty123", "qwerty1", "bartek", "damian", "1qaz2wsx", "qwertyuiop",
    "dragon", "karolina", "abc123", "zxcvbnm", "michal", "samsung", "daniel", "agnieszka",
    "qazwsx", "kacper", "1q2w3e4r", "maciek", "patryk", "1q2w3e", "piotrek", "kasia", "lukasz",
    "kochanie", "dupa", "adrian", "myszka", "master", "mateusz1", "1qazxsw2", "654321",
    "natalia", "komputer", "matrix", "kamil1", "kasia1", "kamil", "madzia", "dupa123", "robert",
    "marcin1", "lolek123", "haslo1", "misiaczek", "haslo", "1234qwer", "niunia", "dominik",
    "wojtek", "pakistan", "klaudia", "bartek1", "paulina", "asdasd", "sebastian", "pokemon",
    "wow12345", "michal1", "weronika", "qwerty12", "kochamcie", "dominika", "barcelona",
    "killer", "monika1", "komputer1", "misiek1", "mariusz", "justyna", "1q2w3e4r5t", "polska123",
    "kamil123", "zaqwsx", "asdfghjkl", "tomek", "szymon", "tomek1", "patrycja", "asdfgh", "dawid",
    "password1", "pawel1", "kosama"
]

# PHONE NUMBERS
def generate_phone_number():
    prefix = str(random.randint(1, 99))
    number = str(random.randint(100000000, 999999999))
    return '+' + prefix + ' ' + number


# EMAIL
def generate_email(login: str, suffix = '@pwr.edu.pl'):
    return login + suffix

# ID_DOCUMENT_TYPE
id_document_types = [
    "passport",
    "id_card"
]

# PESEL
def generate_pesel():
    random.randint()

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

# Generate data for the "departments" table
departments_data = [(name, description) for name, description in departments.items()]
departments_query = "INSERT INTO departments (name, description) VALUES (%s, %s) RETURNING pk_number, name"
for department in departments_data:
    cur.execute(departments_query, department)
    department_id, department_name = cur.fetchone()
    majors = majors_by_department[department_name]
    majors_data = [(major["name"], major["description"], random.randint(50, 180), department_id) for major in majors]
    majors_query = "INSERT INTO majors (nazwa, description, number_of_places, fk_department) VALUES (%s, %s, %s, %s)"
    for major in majors_data:
        cur.execute(majors_query, major)

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
exam_types_data = [(name, minimum_score, maximum_score, multiplier) for name, (minimum_score, maximum_score, multiplier) in exam_types.items()]
exam_types_query = "INSERT INTO exam_types (pk_name, minimum_points_score, maximum_points_score, multiplier) VALUES (%s, %s, %s, %s)"
cur.executemany(exam_types_query, exam_types_data)

# Thresholds
def generate_thresholds():
    majors = majors_by_department.keys()
    thresholds_data = {}
    for m in majors:
        major_id_query = "SELECT pk_number FROM majors WHERE nazwa = %s"
        cur.execute(major_id_query, (m,))
        major_id = cur.fetchone()[0]
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
    'Microsystem Electronics and Photonics': [
        {'Microsystem Electronics': 'Study of microelectronic devices'},
        {'Photonics': 'Study of the generation and manipulation of light'},
    ],
    'Computer Science and Management': [
        {'Computer Science': 'Study of algorithms and programming'},
        {'Information Systems': 'Design and management of information systems'},
        {'Management': 'Study of organizational management principles'},
        {'Cybersecurity': 'Study of securing computer systems and networks'},
    ],
    'Geodesy and Geoinformatics': [
        {'Geodesy': 'Study of Earth\'s geometry and physical properties'},
        {'Geoinformatics': 'Application of information science to spatial data'},
    ],
    'Environmental Engineering': [
        {'Environmental Engineering': 'Environmental impact assessment'},
        {'Ecological Engineering': 'Study of ecological systems and environmental protection'},
    ],
    'Fundamental Problems of Technology': [
        {'Materials Science': 'Study of materials and their properties'},
        {'Nanotechnology': 'Study of manipulation of matter on an atomic, molecular, and supramolecular scale'},
        {'Biotechnology': 'Application of biological systems for technological advancements'},
    ],
    'Pure and Applied Mathematics': [
        {'Pure Mathematics': 'Study of abstract structures and relationships'},
        {'Applied Mathematics': 'Application of mathematical methods to solve real-world problems'},
    ],
    'Mechanical Engineering': [
        {'Mechanical Engineering': 'Design and analysis of mechanical systems'},
        {'Mechatronics': 'Integration of mechanical engineering with electronics and computer science'},
        {'Automotive Engineering': 'Design and production of automotive systems'},
    ],
    'Machines and Transport': [
        {'Machine Construction': 'Design and manufacturing of machines'},
        {'Transportation Engineering': 'Study of transportation systems and infrastructure'},
    ],
    'Materials Engineering': [
        {'Materials Engineering': 'Study of materials and their properties'},
        {'Metallurgy': 'Study of metals and alloys'},
        {'Ceramic Engineering': 'Study of ceramic materials and their applications'},
    ],
    'Mechanical and Power Engineering': [
        {'Power Engineering': 'Study of energy production and utilization'},
        {'Renewable Energy': 'Study of sustainable energy sources'},
        {'Fluid Mechanics': 'Study of fluid behavior'},
    ],
    'Technology and Engineering': [
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
        major_id_query = "SELECT pk_number FROM majors WHERE nazwa = %s"
        cur.execute(major_id_query, (major,))
        major_id = cur.fetchone()[0]
        if not major_id:
            continue
        for course_name, course_description in courses.items():
            course_query = "INSERT INTO courses (name, description, fk_major) VALUES (%s, %s, %s)"
            cur.execute(course_query, (course_name, course_description, major_id))

set_courses()

# ID_DOCUMENT_TYPES
def add_document_types():
    for type in id_document_types:
        query = "INSERT INTO id_document_types (type) VALUES (%s)"
        cur.execute(query, (type,))

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

nationalities_data = [(name, studies_fee_free) for name, studies_fee_free in european_nationalities]
nationalities_query = "INSERT INTO nationalities (pk_name, studies_fee_free) VALUES (%s, %s)"
cur.executemany(nationalities_query, nationalities_data)


# CANDIDATE
def choose_nationality():
    polish_vs_european = [european_nationalities, [{"name": "Polish"}]]
    return random.choice(random.choices(population=polish_vs_european,
                            weights=[0.2, 0.8]))["name"]


def generate_candidates(number_of_candidates):
    for i in range(number_of_candidates):
        candidate_id = i
        login = generate_student_login()
        password = random.choice(passwords)
        name = random.choice(names)
        surname = random.choice(surnames)
        id_document_type: str = random.choices(population=id_document_types,
                                           weights=[0.1, 0.9])
        id_document_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(8, 15)))
        pesel = generate_pesel()
        nationality = choose_nationality()


# SCORING ALGORITHMS
algorithms = [
    {
        "name": "Algorithm for IT majors",
        "factor": 1.0,
    },
    {
        "name": "Algorithm for non-IT majors",
        "factor": 0.8,
    },
    {
        "name": "Algorithm for candidates with disabilities",
        "factor": 1.2,
    }
]
algorithms_data = [(name, factor) for name, factor in algorithms]
algorithms_query = "INSERT INTO scoring_algorithms (name, factor) VALUES (%s, %s)"
cur.executemany(algorithms_query, algorithms_data)

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
    "Geography",
]

subjects_data = [(name,) for name in subject_names]
subjects_query = "INSERT INTO subjects (pk_name) VALUES (%s)"
cur.executemany(subjects_query, subjects_data)



conn.commit()
cur.close()
conn.close()
