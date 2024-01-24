import random

from faker import Faker
from neo4j import GraphDatabase
from random_pesel import RandomPESEL
from logging import Logger

fake = Faker()

URI = "neo4j+s://f53af4cc.databases.neo4j.io"
AUTH = ("neo4j", "1Ob6tEcO0946BsXr9ggRQmVe6834TS68qJikhcTUWJM")

driver = GraphDatabase.driver(URI, auth=AUTH)
driver.verify_connectivity()

def extract_id(executed_query):
    [result], _, [key] = executed_query
    return result[key]


def get_two_way_relationship(first_id, second_id, first_node_name, second_node_name):
    return "\n".join([
        f'Match (node)\n Where ID(node) = {first_id}',
        f'Match (node2)\n Where ID(node2) = {second_id}',
        f'Create (node)-[:{first_node_name}_{second_node_name}]->(node2)',
        f'Create (node2)-[:{second_node_name}_{first_node_name}]->(node)'
    ])

def get_relationship_with_attributes(first_id, second_id, relationship_name, relations_attributes):
    """
    Create a relations with given attributes.
    :param first_id: int
    :param second_id: int
    :param relationship_name: str
    :param relations_attributes: str (in pattern {attr1: "attr1", attr2: "attr2"})
    :return: None
    """
    return "\n".join([
        f'Match (node)\n Where ID(node) = {first_id}',
        f'Match (node2)\n Where ID(node2) = {second_id}',
        'Create (node)-[:%s %s]->(node2)'%(relationship_name, relations_attributes)
    ])


passport = extract_id(driver.execute_query(query_='Create (n:IdDocumentTypes {name:"passport"})\nRETURN ID(n)'))
id_card = extract_id(driver.execute_query(query_='Create (n:IdDocumentTypes {name:"id_card"})\nRETURN ID(n)'))
IdDocumentTypes = [passport, id_card]

RecruitmentExemptionDocumentTypesNames = ["disability_certificate", "certificate_of_completion_of_the_first_degree", "certificate_of_completion_of_the_second_degree",
"certificate_of_completion_of_the_third_degree", "studium_talent"]
RecruitmentExemptionDocumentTypes = []
for name in RecruitmentExemptionDocumentTypesNames:
    RecruitmentExemptionDocumentTypes.append(extract_id(driver.execute_query('CREATE (n:RecruitmentExemptionDocumentTypes {name: "%s"})\nRETURN ID(n)'%(name))))

FeesExemptionDocumentTypesNames = ["disability_certificate", "certificate_of_completion_of_the_first_degree", "certificate_of_completion_of_the_second_degree"]
FeesExemptionDocumentTypes = []
for name in FeesExemptionDocumentTypesNames:
    FeesExemptionDocumentTypes.append(extract_id(driver.execute_query('CREATE (n:FeesExemptionDocumentTypes {name: "%s"})\nRETURN ID(n)'%(name))))

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
algorithms = ["Algorithm for IT majors", "Algorithm for non-IT majors", "Algorithm for geodesy majors",
              "Algorithm for humanities majors", "Algorithm for natural sciences majors",
              "Algorithms for language majors"]

MajorAlgorithms = []
for algorithm in algorithms:
    MajorAlgorithms.append(extract_id(driver.execute_query('CREATE (n:MajorAlgorithms {name: "%s"})\nRETURN ID(n)'%(algorithm))))


departments_data = [(name, description) for name, description in departments.items()]
departments_query = "INSERT INTO departments (name, description) VALUES (%s, %s) RETURNING pk_number, name"

Departments = []
Majors = []
for name, description in departments_data:
    department_id = extract_id(driver.execute_query(
        'CREATE (n:Departments {name: "%s", description: "%s"})\nRETURN ID(n)'%(name, description)))
    Departments.append(department_id)
    majors = majors_by_department[name]
    for major in majors:
        major_id = extract_id(driver.execute_query(
            'CREATE (n:Majors {name: "%s", description: "%s", number_of_places: %s})\nRETURN ID(n)'%(major['name'], major['description'], random.randint(50, 180))
        ))
        Majors.append(major_id)
        driver.execute_query(get_two_way_relationship(major_id, department_id, "MAJORS", "DEPARTMENTS"))
        driver.execute_query(get_two_way_relationship(major_id, random.choices(MajorAlgorithms, weights=[4, 10, 4, 1, 2, 1])[0], "MAJORS", "MAJOR_ALGORITHMS"))

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

ExamTypes = []
for name, data in exam_types.items():
    ExamTypes.append(extract_id(driver.execute_query(
        'CREATE (n:ExamTypes {name: "%s", multiplier: %s, minimum_points_score: %s, maximum_points_score: %s})\nRETURN ID(n)'
            %(name, data["multiplier"], data["minimum_score"], data["maximum_score"])
    )))

# Thresholds
def generate_thresholds():
    thresholds_data = {}
    for major_id in Majors:
        for year in range(2018, 2023):
            previous_year_thresholds = [(major_id, year)] if (major_id, year) in thresholds_data else round(
                random.uniform(20, 500), 1)
            first_round = min(max(previous_year_thresholds + round(random.uniform(-50, 50), 1), 20.0), 500.0)
            second_round = min(max(first_round + round(random.uniform(-50, 50), 1), 20.0), 500.0)
            third_round = min(max(second_round + round(random.uniform(-50, 50), 1), 20.0), 500.0)
            thresholds_data.update({
                (major_id, year): {
                    "round_1": first_round,
                    "round_2": second_round,
                    "round_3": third_round}
            })
    return thresholds_data


Thresholds = []
thresholds = generate_thresholds()
for key, value in thresholds.items():
    major_id, year = key

    thresholds_id = extract_id(driver.execute_query(
        'CREATE (n:Thresholds {year: %s, round_1: %s, round_2: %s, round_3: %s})\nRETURN ID(n)'
            %(year, value["round_1"], value["round_2"], value["round_3"])
    ))
    Thresholds.append(thresholds_id)
    get_two_way_relationship(thresholds_id, major_id, "THRESHOLDS", "MAJOR")

print("Thresholds added")
# COURSE
majors_with_courses = {
    'Architecture': [
        'Architectural Design',
        'Architectural History',
        'Building Technology',
        'Urban Design',
        'Sustainable Architecture'
    ],
    'Urban Planning': [
        'Urban Planning and Design',
        'Land Use Policy',
        'Transportation Planning',
        'Community Development',
        'Environmental Planning'
    ],
    'Interior Design': [
        'Interior Design Fundamentals',
        'Space Planning',
        'Color Theory',
        'Furniture Design',
        'Interior Lighting'
    ],
    'Civil Engineering': [
        'Structural Engineering',
        'Transportation Engineering',
        'Geotechnical Engineering',
        'Environmental Engineering',
        'Construction Management'
    ],
    'Structural Engineering': [
        'Advanced Structural Analysis',
        'Structural Design',
        'Seismic Engineering',
        'Bridge Engineering',
        'Steel and Concrete Structures'
    ],
    'Chemistry': [
        'Inorganic Chemistry',
        'Organic Chemistry',
        'Physical Chemistry',
        'Analytical Chemistry',
        'Biochemistry'
    ],
    'Biochemistry': [
        'Biochemical Pathways',
        'Enzyme Kinetics',
        'Protein Structure and Function',
        'Molecular Biology',
        'Biotechnology'
    ],
    'Electronics': [
        'Electronic Circuits',
        'Digital Electronics',
        'Analog Electronics',
        'Microelectronics',
        'VLSI Design'
    ],
    'Digital Systems': [
        'Digital System Design',
        'Embedded Systems',
        'FPGA Programming',
        'Digital Signal Processing',
        'Hardware-Software Co-design'
    ],
    'Electrical Engineering': [
        'Electric Circuits',
        'Electromagnetic Fields',
        'Power Electronics',
        'Control Systems',
        'Renewable Energy Systems'
    ],
    'Power Systems': [
        'Power System Analysis',
        'Power System Protection',
        'Smart Grids',
        'High Voltage Engineering',
        'Power System Planning'
    ],
    'Control Systems': [
        'Control System Design',
        'Robotics and Automation',
        'Process Control',
        'Optimal Control',
        'Adaptive Control'
    ],
    'Microsystem Electronics': [
        'Microfabrication Techniques',
        'MEMS Design',
        'Nanoelectronics',
        'Integrated Circuit Design',
        'Sensors and Actuators'
    ],
    'Photonics': [
        'Optical Fiber Communication',
        'Laser Systems',
        'Photonic Materials',
        'Optoelectronics',
        'Photonics Applications'
    ],
    'Computer Science': [
        'Algorithms and Data Structures',
        'Software Development',
        'Database Systems',
        'Machine Learning',
        'Artificial Intelligence'
    ],
    'Information Systems': [
        'Information System Design',
        'Database Management',
        'Business Intelligence',
        'Enterprise Systems',
        'Information Security'
    ],
    'Management': [
        'Principles of Management',
        'Organizational Behavior',
        'Strategic Management',
        'Human Resource Management',
        'Project Management'
    ],
    'Cybersecurity': [
        'Network Security',
        'Cyber Threat Intelligence',
        'Digital Forensics',
        'Security Policy and Compliance',
        'Ethical Hacking'
    ],
    'Geodesy': [
        'Geodetic Measurements',
        'Geospatial Data Analysis',
        'Satellite Geodesy',
        'Cartography',
        'Geodetic Surveying'
    ],
    'Geoinformatics': [
        'Geographic Information Systems (GIS)',
        'Remote Sensing',
        'Spatial Analysis',
        'Geospatial Database Management',
        'Web Mapping'
    ],
    'Environmental Engineering': [
        'Water and Wastewater Treatment',
        'Air Quality Management',
        'Environmental Impact Assessment',
        'Solid Waste Management',
        'Environmental Remediation'
    ],
    'Ecological Engineering': [
        'Ecosystem Restoration',
        'Sustainable Land Use',
        'Wetland Ecology',
        'Ecological Modeling',
        'Wildlife Conservation'
    ],
    'Materials Science': [
        'Materials Characterization',
        'Materials Processing',
        'Nanomaterials',
        'Materials Testing',
        'Materials for Renewable Energy'
    ],
    'Nanotechnology': [
        'Introduction to Nanoscience',
        'Nanomaterials Synthesis',
        'Nanoelectronics',
        'Nanomedicine',
        'Nanotechnology Applications'
    ],
    'Biotechnology': [
        'Genetic Engineering',
        'Bioprocess Engineering',
        'Biopharmaceuticals',
        'Biotechnology Ethics',
        'Biotechnology Entrepreneurship'
    ],
    'Pure Mathematics': [
        'Calculus',
        'Linear Algebra',
        'Abstract Algebra',
        'Real Analysis',
        'Number Theory'
    ],
    'Applied Mathematics': [
        'Differential Equations',
        'Numerical Methods',
        'Mathematical Modeling',
        'Probability and Statistics',
        'Operations Research'
    ],
    'Mechanical Engineering': [
        'Thermodynamics',
        'Fluid Mechanics',
        'Machine Design',
        'Manufacturing Processes',
        'Mechanical Vibrations'
    ],
    'Mechatronics': [
        'Control Systems for Mechatronics',
        'Robotics and Automation',
        'Sensors and Actuators',
        'Embedded Systems',
        'Mechatronics Design'
    ],
    'Automotive Engineering': [
        'Automotive Design',
        'Vehicle Dynamics',
        'Automotive Safety',
        'Powertrains and Propulsion Systems',
        'Vehicle Electronics'
    ],
    'Machine Construction': [
        'Machine Design',
        'Manufacturing Processes',
        'Material Science',
        'Mechanical Analysis',
        'Machine Automation'
    ],
    'Transportation Engineering': [
        'Traffic Engineering',
        'Transportation Planning',
        'Public Transportation Systems',
        'Transportation Infrastructure',
        'Transportation Safety'
    ],
    'Materials Engineering': [
        'Materials Characterization',
        'Materials Processing',
        'Nanomaterials',
        'Materials Testing',
        'Materials for Renewable Energy'
    ],
    'Metallurgy': [
        'Physical Metallurgy',
        'Extractive Metallurgy',
        'Metal Forming',
        'Metal Casting',
        'Metallurgical Analysis'
    ],
    'Ceramic Engineering': [
        'Ceramic Materials',
        'Ceramic Processing',
        'Refractory Technology',
        'Advanced Ceramics',
        'Ceramic Design'
    ],
    'Power Engineering': [
        'Electric Power Generation',
        'Power System Analysis',
        'High Voltage Engineering',
        'Renewable Energy Systems',
        'Power Electronics'
    ],
    'Renewable Energy': [
        'Solar Energy Systems',
        'Wind Energy Technology',
        'Hydropower Engineering',
        'Biomass Energy',
        'Energy Storage Systems'
    ],
    'Fluid Mechanics': [
        'Fluid Dynamics',
        'Heat Transfer',
        'Turbomachinery',
        'Computational Fluid Dynamics',
        'Fluid Flow and Transport Phenomena'
    ],
    'Robotics': [
        'Robotics Fundamentals',
        'Robot Kinematics and Dynamics',
        'Machine Vision',
        'Control of Robotic Systems',
        'Robotic Programming'
    ],
    'Applied Informatics': [
        'Information Systems Development',
        'Data Management',
        'Software Engineering',
        'Business Information Systems',
        'Applied Informatics Projects'
    ],
    'Data Science': [
        'Data Analysis and Visualization',
        'Machine Learning',
        'Big Data Technologies',
        'Data Mining',
        'Deep Learning and Neural Networks'
    ],
    'Organization and Management': [
        'Organizational Theory',
        'Management Principles',
        'Strategic Planning',
        'Leadership and Change Management',
        'Organizational Behavior'
    ],
    'Project Management': [
        'Project Planning and Scheduling',
        'Project Risk Management',
        'Agile Project Management',
        'Project Quality Management',
        'Project Procurement Management'
    ],
    'Human Resource Management': [
        'Human Resource Planning',
        'Talent Management',
        'Compensation and Benefits',
        'Employee Relations',
        'Diversity and Inclusion in the Workplace'
    ]
}

course_descriptions = {

    'Machine Design': 'Learn the principles and techniques of designing machines and mechanical systems.',
    'Manufacturing Processes': 'Study the various processes used in manufacturing, including machining, forming, and assembly.',
    'Architectural Design': 'This course covers the principles and techniques of architectural design, focusing on creating functional and aesthetically pleasing structures.',
    'Architectural History': 'Explore the history of architecture, including different styles, periods, and significant architectural movements.',
    'Building Technology': 'Learn about the technology and materials used in the construction of buildings and structures.',
    'Urban Design': 'Study the design of urban environments, considering factors such as city layout, transportation, and public spaces.',
    'Sustainable Architecture': 'Examine sustainable and eco-friendly practices in architecture and design to create environmentally responsible structures.',
    'Urban Planning and Design': 'This course explores the planning and design of urban areas, addressing issues like zoning, transportation, and land use.',
    'Land Use Policy': 'Learn about policies and regulations related to land use, zoning, and urban development.',
    'Transportation Planning': 'Focus on planning and managing transportation systems in urban areas, including roads, public transportation, and traffic management.',
    'Community Development': 'Explore strategies for community development, including housing, infrastructure, and community engagement.',
    'Environmental Planning': 'Study the integration of environmental considerations into urban planning and development processes.',
    'Interior Design Fundamentals': 'Learn the basics of interior design, including space planning, color theory, and furniture selection.',
    'Space Planning': 'Focus on effective space planning in interior design, considering functionality and aesthetics.',
    'Color Theory': 'Understand the principles of color theory and how it applies to interior design and visual aesthetics.',
    'Furniture Design': 'Explore the design and selection of furniture for interior spaces, considering form and function.',
    'Interior Lighting': 'Study the principles of lighting design and how it impacts the ambiance of interior spaces.',
    'Structural Engineering': 'Learn about the principles of structural engineering, including the analysis and design of building structures.',
    'Transportation Engineering': 'Focus on engineering aspects of transportation systems, including road design, traffic flow, and safety.',
    'Geotechnical Engineering': 'Study the behavior of soil and rock materials, especially in the context of construction and foundation design.',
    'Environmental Engineering': 'Explore the field of environmental engineering, which focuses on solving environmental issues through engineering solutions.',
    'Construction Management': 'Learn about project management and logistics in the construction industry.',
    'Advanced Structural Analysis': 'This course delves deeper into structural analysis techniques and methods.',
    'Structural Design': 'Focus on the design of building structures, considering factors such as load-bearing capacity and safety.',
    'Seismic Engineering': 'Study the engineering of structures to withstand seismic forces and earthquakes.',
    'Bridge Engineering': 'Learn about the design and construction of bridges, considering structural and transportation engineering aspects.',
    'Steel and Concrete Structures': 'Explore the use of steel and concrete in building and bridge construction.',
    'Inorganic Chemistry': 'An introduction to the study of inorganic chemistry, covering the properties and reactions of inorganic compounds.',
    'Organic Chemistry': 'Study the structure, properties, and reactions of organic compounds, including hydrocarbons and functional groups.',
    'Physical Chemistry': 'Explore the physical principles that underlie chemical processes and reactions.',
    'Analytical Chemistry': 'Learn techniques for chemical analysis, including qualitative and quantitative analysis methods.',
    'Biochemistry': 'This course covers the chemistry of biological molecules and processes, including enzymes, DNA, and metabolism.',
    'Biochemical Pathways': 'Explore the metabolic pathways and processes that occur within living organisms.',
    'Enzyme Kinetics': 'Study the kinetics and mechanisms of enzyme-catalyzed reactions.',
    'Protein Structure and Function': 'Learn about the structure and function of proteins, including their role in biological systems.',
    'Molecular Biology': 'Explore the study of molecular processes in living organisms, including DNA replication and gene expression.',
    'Biotechnology': 'Learn about the applications of biotechnology in areas such as medicine, agriculture, and industry.',
    'Electronic Circuits': 'This course covers the principles of electronic circuits, including circuit analysis and design.',
    'Digital Electronics': 'Study the digital electronic components and circuits used in computers and digital systems.',
    'Analog Electronics': 'Learn about analog electronic circuits, including amplifiers, filters, and signal processing.',
    'Microelectronics': 'Focus on the design and fabrication of microelectronic devices and integrated circuits.',
    'VLSI Design': 'Study very large-scale integration (VLSI) design techniques for creating complex integrated circuits.',
    'Digital System Design': 'Explore the design of digital systems, including hardware and software components.',
    'Embedded Systems': 'Learn about embedded systems design, which involves creating specialized computer systems for specific tasks.',
    'FPGA Programming': 'Focus on programming field-programmable gate arrays (FPGAs) for custom digital logic design.',
    'Digital Signal Processing': 'Study the processing of digital signals and their applications in various fields.',
    'Hardware-Software Co-design': 'Explore the integration of hardware and software components in system design.',
    'Electric Circuits': 'Learn about the fundamental principles of electric circuits, including analysis and circuit elements.',
    'Electromagnetic Fields': 'Study the behavior of electromagnetic fields and their applications in various technologies.',
    'Power Electronics': 'Explore the design and control of power electronic systems, including converters and inverters.',
    'Control Systems': 'Learn about control theory and the design of control systems for various applications.',
    'Renewable Energy Systems': 'Focus on the design and implementation of renewable energy systems, including solar and wind power.',
    'Power System Analysis': 'Study the analysis of power distribution systems and their stability and performance.',
    'Power System Protection': 'Explore the protection of power systems against faults and disturbances.',
    'Smart Grids': 'Learn about smart grid technologies and their role in modern energy distribution.',
    'High Voltage Engineering': 'Study the principles and technologies related to high-voltage electrical systems.',
    'Power System Planning': 'Focus on the planning and optimization of electrical power systems.',
    'Control System Design': 'This course covers the design of control systems for various applications, emphasizing stability and performance.',
    'Robotics and Automation': 'Explore the field of robotics and automation, including robot design and programming.',
    'Process Control': 'Learn about the control of industrial processes, including monitoring and optimization.',
    'Optimal Control': 'Study optimal control theory and its application in controlling dynamic systems.',
    'Adaptive Control': 'Focus on adaptive control strategies that can adjust to changing system conditions.',
    'Microfabrication Techniques': 'Learn about the techniques used in microfabrication for creating small-scale devices and structures.',
    'MEMS Design': 'Explore the design of microelectromechanical systems (MEMS) for various applications.',
    'Nanoelectronics': 'Study the field of nanoelectronics, which deals with electronic devices at the nanoscale.',
    'Integrated Circuit Design': 'Focus on the design of integrated circuits (ICs) for electronic devices.',
    'Optical Fiber Communication': 'Study the principles and technologies of optical fiber communication systems.',
    'Laser Systems': 'Explore the use of lasers in various applications, including communication, medical procedures, and manufacturing.',
    'Photonic Materials': 'Learn about the materials used in photonics, including their properties and applications in optical devices.',
    'Optoelectronics': 'Focus on optoelectronic devices and their use in applications like displays, sensors, and communication systems.',
    'Photonics Applications': 'Explore practical applications of photonics technology in areas such as telecommunications, imaging, and sensing.',
    'Algorithms and Data Structures': 'Study fundamental algorithms and data structures used in computer science and programming.',
    'Software Development': 'Learn the principles and best practices of software development, including coding, testing, and debugging.',
    'Database Systems': 'Explore the design and management of database systems, including relational databases and SQL.',
    'Machine Learning': 'Study the concepts and techniques of machine learning for pattern recognition and prediction.',
    'Artificial Intelligence': 'Learn about the fundamentals of artificial intelligence, including knowledge representation, reasoning, and problem-solving.',
    'Information System Design': 'Focus on the design and development of information systems for organizational use.',
    'Database Management': 'Explore advanced topics in database management, including optimization and security.',
    'Business Intelligence': 'Learn how to gather, analyze, and present business data for decision-making purposes.',
    'Enterprise Systems': 'Explore the implementation and management of enterprise-level information systems in organizations.',
    'Information Security': 'Study strategies and technologies for securing digital information and systems from threats and attacks.',
    'Principles of Management': 'Learn the fundamental principles of management, including planning, organizing, and leading.',
    'Organizational Behavior': 'Explore the psychology and behavior of individuals and groups in organizational settings.',
    'Strategic Management': 'Study strategic planning and decision-making in organizations to achieve long-term goals.',
    'Human Resource Management': 'Focus on the management of an organization\'s human resources, including recruitment, training, and performance evaluation.',
    'Project Management': 'Learn project management methodologies and techniques for successful project completion.',
    'Network Security': 'Study the principles and practices of securing computer networks and data from cyber threats.',
    'Cyber Threat Intelligence': 'Explore the collection and analysis of intelligence related to cybersecurity threats and vulnerabilities.',
    'Digital Forensics': 'Learn the techniques used in digital forensics to investigate and analyze digital evidence in legal and investigative contexts.',
    'Security Policy and Compliance': 'Focus on developing and implementing security policies and ensuring compliance with relevant regulations and standards.',
    'Ethical Hacking': 'Explore ethical hacking techniques used to identify and address security vulnerabilities in computer systems.',
    'Geodetic Measurements': 'Learn about geodetic surveying and measurements for accurately determining positions and distances on Earth.',
    'Geospatial Data Analysis': 'Focus on the analysis and interpretation of geospatial data using GIS and other tools.',
    'Satellite Geodesy': 'Study the use of satellite technology for geodetic measurements and mapping.',
    'Cartography': 'Learn the principles and techniques of mapmaking, including cartographic design and map production.',
    'Geodetic Surveying': 'Explore surveying techniques used in geodesy and land mapping.',
    'Geographic Information Systems (GIS)': 'Study the use of GIS technology for spatial data analysis, mapping, and visualization.',
    'Remote Sensing': 'Explore remote sensing methods for collecting data about the Earth\'s surface from a distance.',
    'Spatial Analysis': 'Focus on spatial data analysis techniques to extract meaningful information from geographic data.',
    'Geospatial Database Management': 'Learn about database management techniques for geospatial data, including storage and retrieval.',
    'Web Mapping': 'Explore web-based mapping applications and services for displaying and sharing geospatial data.',
    'Water and Wastewater Treatment': 'Study the processes and technologies used in water and wastewater treatment and purification.',
    'Air Quality Management': 'Learn about strategies for monitoring and improving air quality in various environments.',
    'Environmental Impact Assessment': 'Explore the assessment of environmental impacts of projects and activities on ecosystems and communities.',
    'Solid Waste Management': 'Focus on the management and disposal of solid waste and strategies for waste reduction and recycling.',
    'Environmental Remediation': 'Study techniques and methods for cleaning up contaminated sites and restoring environmental quality.',
    'Ecosystem Restoration': 'Learn about the restoration and conservation of ecosystems to promote biodiversity and ecological health.',
    'Sustainable Land Use': 'Explore sustainable land use and development practices that balance human needs with environmental conservation.',
    'Wetland Ecology': 'Study the ecology and conservation of wetlands, including the importance of these ecosystems.',
    'Ecological Modeling': 'Focus on ecological modeling techniques for understanding and predicting ecosystem dynamics.',
    'Wildlife Conservation': 'Learn about strategies and practices for conserving and protecting wildlife and their habitats.',
    'Materials Characterization': 'Explore techniques for analyzing and characterizing the properties of materials at the microscopic and macroscopic levels.',
    'Materials Processing': 'Learn about various methods of processing materials, including shaping, forming, and manufacturing processes.',
    'Nanomaterials': 'Study nanomaterials, which have unique properties at the nanoscale, and their applications in various fields.',
    'Materials Testing': 'Focus on the testing and evaluation of materials for quality control and performance assessment.',
    'Materials for Renewable Energy': 'Explore materials used in renewable energy technologies, such as solar cells and energy storage devices.',
    'Introduction to Nanoscience': 'Learn the fundamentals of nanoscience, which explores phenomena and materials at the nanoscale.',
    'Nanomaterials Synthesis': 'Study techniques for synthesizing nanomaterials with specific properties and structures.',
    'Nanomedicine': 'Learn about the application of nanotechnology in medicine, including drug delivery and diagnostics.',
    'Nanotechnology Applications': 'Focus on various practical applications of nanotechnology in different industries and fields.',
    'Genetic Engineering': 'Study the principles and techniques of genetic engineering for modifying and manipulating genetic material.',
    'Bioprocess Engineering': 'Learn about the engineering of biological processes, such as fermentation and bioproduction.',
    'Biopharmaceuticals': 'Explore the development and production of biopharmaceutical drugs and products.',
    'Biotechnology Ethics': 'Discuss ethical considerations and issues related to biotechnology and genetic engineering.',
    'Biotechnology Entrepreneurship': 'Learn about entrepreneurship and business aspects in the field of biotechnology.',
    'Calculus': 'Study the fundamentals of calculus, including differentiation and integration of functions.',
    'Linear Algebra': 'Explore the algebraic properties of vectors and matrices and their applications in mathematics and science.',
    'Abstract Algebra': 'Learn about advanced algebraic structures and concepts, including groups, rings, and fields.',
    'Real Analysis': 'Study the theory of real numbers, sequences, and limits in mathematical analysis.',
    'Number Theory': 'Explore number theory, which focuses on the properties and relationships of integers and prime numbers.',
    'Differential Equations': 'Learn about differential equations and their solutions, including ordinary and partial differential equations.',
    'Numerical Methods': 'Focus on numerical techniques and algorithms for solving mathematical problems and simulations.',
    'Mathematical Modeling': 'Study the creation and analysis of mathematical models to describe real-world phenomena.',
    'Probability and Statistics': 'Explore probability theory and statistical methods for data analysis and inference.',
    'Operations Research': 'Learn about the application of mathematical and analytical methods to solve complex decision-making problems.',
    'Thermodynamics': 'Study the principles of thermodynamics, including energy, heat, and work in physical systems.',
    'Fluid Mechanics': 'Explore the behavior of fluids (liquids and gases) and their properties in various applications.',
    'Mechanical Vibrations': 'Explore the analysis and control of mechanical vibrations in engineering systems.',
    'Control Systems for Mechatronics': 'Learn about control systems used in mechatronic devices and systems.',
    'Mechatronics Design': 'Focus on the design and integration of mechatronic systems, combining mechanical and electronic components.',
    'Automotive Design': 'Explore the design and engineering of automotive vehicles, including cars and trucks.',
    'Vehicle Dynamics': 'Study the dynamics and behavior of vehicles, including handling and performance characteristics.',
    'Automotive Safety': 'Learn about safety features and systems in automotive design to enhance vehicle safety.',
    'Powertrains and Propulsion Systems': 'Explore the powertrains and propulsion systems used in automotive vehicles.',
    'Vehicle Electronics': 'Focus on the electronic systems and components used in modern vehicles.',
    'Material Science': 'Explore the science of materials, including their properties, behavior, and applications.',
    'Mechanical Analysis': 'Study the analysis of mechanical systems and structures, including stress and deformation analysis.',
    'Machine Automation': 'Learn about the automation of machines and processes for increased efficiency and productivity.',
    'Traffic Engineering': 'Focus on the planning and management of traffic systems and transportation infrastructure.',
    'Public Transportation Systems': 'Explore the design and management of public transportation systems for urban areas.',
    'Transportation Infrastructure': 'Learn about the infrastructure required for transportation, including roads, bridges, and airports.',
    'Transportation Safety': 'Focus on safety measures and regulations in transportation to reduce accidents and risks.',
    'Physical Metallurgy': 'Study the physical properties and behavior of metallic materials, including their structure and processing.',
    'Extractive Metallurgy': 'Learn about the extraction of metals from ores and their refining and processing.',
    'Metal Forming': 'Explore techniques for shaping and forming metals into desired shapes and structures.',
    'Metal Casting': 'Study the casting process, which involves pouring molten metal into molds to create components.',
    'Metallurgical Analysis': 'Learn about the analysis of metals and alloys to determine their composition and properties.',
    'Ceramic Materials': 'Explore the properties and applications of ceramic materials in various industries.',
    'Ceramic Processing': 'Learn about the processing and shaping of ceramic materials for different applications.',
    'Refractory Technology': 'Focus on refractory materials used in high-temperature industrial applications.',
    'Advanced Ceramics': 'Study advanced ceramic materials and their applications in cutting-edge technologies.',
    'Ceramic Design': 'Learn about the design and engineering of ceramic products and components.',
    'Electric Power Generation': 'Explore the generation of electric power from various sources, including fossil fuels and renewable energy.',
    'Solar Energy Systems': 'Study the technology and design of solar energy systems for electricity generation and heating.',
    'Wind Energy Technology': 'Learn about the principles and technology of wind energy systems for clean power generation.',
    'Hydropower Engineering': 'Focus on the engineering and design of hydropower systems for energy production.',
    'Biomass Energy': 'Explore the use of biomass materials for energy generation and their environmental impact.',
    'Energy Storage Systems': 'Learn about energy storage technologies, including batteries and energy management systems.',
    'Fluid Dynamics': 'Study the behavior of fluids in motion, including the principles of fluid flow and pressure.',
    'Heat Transfer': 'Explore the principles of heat transfer, including conduction, convection, and radiation.',
    'Turbomachinery': 'Learn about turbomachines, such as turbines and compressors, used in fluid handling and energy conversion.',
    'Computational Fluid Dynamics': 'Focus on the use of computer simulations and modeling for fluid flow analysis and prediction.',
    'Fluid Flow and Transport Phenomena': 'Study the transport of materials and heat in fluid systems, including mass and energy transfer.',
    'Robotics Fundamentals': 'Learn the fundamental concepts and principles of robotics, including robot kinematics and dynamics.',
    'Robot Kinematics and Dynamics': 'Explore the kinematics and dynamics of robot motion and control.',
    'Machine Vision': 'Learn about computer vision techniques used in robotics for perception and object recognition.',
    'Control of Robotic Systems': 'Focus on the control and operation of robotic systems in various applications.',
    'Robotic Programming': 'Explore the programming and software development for controlling and operating robots.',
    'Information Systems Development': 'Learn the process of developing information systems, including requirements analysis and software design.',
    'Data Management': 'Study data management techniques and practices, including database design and administration.',
    'Software Engineering': 'Explore software engineering principles and methodologies for software development.',
    'Business Information Systems': 'Learn how information systems are used to support business processes and decision-making.',
    'Applied Informatics Projects': 'Focus on practical projects in the field of informatics, including software development and system integration.',
    'Data Analysis and Visualization': 'Learn data analysis techniques and data visualization for understanding and presenting data.',
    'Big Data Technologies': 'Explore technologies and tools for handling and analyzing large-scale data sets.',
    'Data Mining': 'Learn about data mining techniques for discovering patterns and trends in data.',
    'Deep Learning and Neural Networks': 'Study deep learning methods and neural network architectures for complex data analysis.',
    'Organizational Theory': 'Explore theories and concepts related to the structure and behavior of organizations.',
    'Management Principles': 'Learn fundamental principles of management, including planning, organizing, and leading organizations.',
    'Strategic Planning': 'Study the process of strategic planning and decision-making to achieve long-term organizational goals.',
    'Leadership and Change Management': 'Focus on leadership strategies and managing organizational change effectively.',
    'Project Planning and Scheduling': 'Learn project planning and scheduling techniques for effective project management.',
    'Project Risk Management': 'Focus on managing risks and uncertainties in project management to ensure project success.',
    'Agile Project Management': 'Explore Agile project management methodologies for adaptive and iterative project development.',
    'Project Quality Management': 'Learn about quality management principles and practices in project management.',
    'Project Procurement Management': 'Focus on the procurement and contract management aspects of project execution.',
    'Human Resource Planning': 'Explore human resource planning and management, including recruitment and talent management.',
    'Talent Management': 'Learn about strategies for attracting, developing, and retaining talent within organizations.',
    'Compensation and Benefits': 'Study compensation and benefits strategies and practices for employee motivation and retention.',
    'Employee Relations': 'Focus on maintaining positive employee relations and managing workplace conflicts.',
    'Diversity and Inclusion in the Workplace': 'Explore diversity and inclusion practices for creating inclusive and equitable workplaces.',
    'Sensors and Actuators': 'Explore the world of devices that sense and respond to the physical environment in this course.'
}


Courses = []
for major_name, courses in majors_with_courses.items():
    major_id = extract_id(driver.execute_query(
        'MATCH (major:Majors)\nWHERE major.name = "%s"\nRETURN ID(major)'
        % major_name
    ))
    if not major_id:
        continue

    for course in courses:
        course_name = course
        course_description = course_descriptions[course_name]
        course_id = extract_id(driver.execute_query(
            'MATCH (major: Majors)\n WHERE ID(major) = %s \nCREATE (n:Courses {name: "%s", description: "%s"})\nRETURN ID(n)'
            % (major_id, course_name, course_description)
        ))
        Courses.append(course_id)
        get_two_way_relationship(course_id, major_id, "COURSES", "MAJORS")


# NATIONALITIES
european_nationalities = [
    {"name": "Albanian", "studies_fee_free": False},
    {"name": "Austrian", "studies_fee_free": True},
    {"name": "Belgian", "studies_fee_free": True},
    {"name": "Belarusian", "studies_fee_free": False},
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

Nationalities = []
for nationality in european_nationalities:
    Nationalities.append(extract_id(driver.execute_query(
            'CREATE (n:Nationalities {name: "%s", studies_fee_free: %s})\nRETURN ID(n)'
            % (nationality["name"], nationality["studies_fee_free"])
        )))


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
    "Geography",
    "Philosophy",
    "Music history",
    "Art history",
    "Social studies",
    "Foreign languages"
]

Subjects = []
for subject_name in subject_names:
    Subjects.append(extract_id(driver.execute_query(
        'CREATE (n:Subjects {name: "%s"})\nRETURN ID(n)'
        % subject_name
    )))

print("SUBJECTS added")
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
    },
    {
        "fk_subject": "Literature",
        "fk_algorithm": "Algorithm for humanities majors",
        "factor": 3.0
    },
    {
        "fk_subject": "Art",
        "fk_algorithm": "Algorithm for humanities majors",
        "factor": 0.5
    },
    {
        "fk_subject": "History",
        "fk_algorithm": "Algorithm for humanities majors",
        "factor": 2.0
    },
    {
        "fk_subject": "Philosophy",
        "fk_algorithm": "Algorithm for humanities majors",
        "factor": 0
    },
    {
        "fk_subject": "Music history",
        "fk_algorithm": "Algorithm for humanities majors",
        "factor": 0.5
    },
    {
        "fk_subject": "Art history",
        "fk_algorithm": "Algorithm for humanities majors",
        "factor": 0.5
    },
    {
        "fk_subject": "Social studies",
        "fk_algorithm": "Algorithm for humanities majors",
        "factor": 0.75
    },
    {
        "fk_subject": "Foreign languages",
        "fk_algorithm": "Algorithm for humanities majors",
        "factor": 0.25
    },
    {
        "fk_subject": "Foreign languages",
        "fk_algorithm": "Algorithm for natural sciences majors",
        "factor": 0.25
    },
    {
        "fk_subject": "Biology",
        "fk_algorithm": "Algorithm for natural sciences majors",
        "factor": 0.5
    },
    {
        "fk_subject": "Chemistry",
        "fk_algorithm": "Algorithm for natural sciences majors",
        "factor": 0.5
    },
    {
        "fk_subject": "Mathematics",
        "fk_algorithm": "Algorithm for natural sciences majors",
        "factor": 0.5
    },
    {
        "fk_subject": "Physics",
        "fk_algorithm": "Algorithm for natural sciences majors",
        "factor": 0.5
    },
    {
        "fk_subject": "Foreign languages",
        "fk_algorithm": "Algorithms for language majors",
        "factor": 2.0
    },
    {
        "fk_subject": "Literature",
        "fk_algorithm": "Algorithms for language majors",
        "factor": 0.5
    },
    {
        "fk_subject": "Philosophy",
        "fk_algorithm": "Algorithms for language majors",
        "factor": 0.5
    }
]


# SUBJECTS_MENTIONED_IN_ALGORITHM
for subject_algorithm_factor in subjects_mentioned_in_algorithm:
    driver.execute_query(
        'MATCH (subject:Subjects)\n WHERE subject.name = "%s"\n'
        'MATCH (a:MajorAlgorithms)\n WHERE a.name = "%s"\n'
        'CREATE (n:SUBJECTS_MENTIONED_IN_ALGORITHM {factor: %s})'
        % (subject_algorithm_factor["fk_subject"], subject_algorithm_factor["fk_algorithm"], subject_algorithm_factor["factor"])
    )

fake = Faker()
fake_pesel = RandomPESEL()

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


print("SUBJECTS_MENTIONED_IN_ALGORITHM added")
def generate_candidate_account():
    login = fake.unique.pystr_format(string_format='pwr??????', letters='1234567890')
    password = fake.password()
    query = 'CREATE (account: Accounts {login: "%s", password: "%s"})\n RETURN ID(account)'%(login, password)
    return extract_id(driver.execute_query(query_=query))


def get_document_type_with_nationality():
    is_polish = random.choices([True, False], weights=[0.9, 0.1])[0]
    if is_polish:
        return "id_card", "Polish"
    else:
        return "passport", random.choice(Nationalities)


def generate_exam_results(candidate_id):
    document_id = fake.pystr(min_chars=6, max_chars=20)
    date = fake.date_between(start_date='-5y', end_date='today')
    exam_type = random.choice(ExamTypes)
    query = 'Create (e:Exams {documentId: "%s", date: date("%s")})\n RETURN ID(e)'%(document_id, date)
    exam_id = extract_id(driver.execute_query(query_=query))
    generate_subject_results(exam_id, exam_type)
    query2 = get_two_way_relationship(candidate_id, exam_id, "CANDIDATE", "EXAM")
    driver.execute_query(query_=query2)


def generate_subject_results(exam_id, exam_type):
    subject_len = random.randint(1, 5)
    subjects = random.choices(Subjects, k=subject_len)
    for subject in subjects:
        points = random.randint(exam_types[exam_type[0]]["minimum_score"], exam_types[exam_type[0]]["maximum_score"])
        query = get_relationship_with_attributes(exam_id, subject, "SUBJECTS_RESULTS", "{points: %s}" % points)
        driver.execute_query(query_=query)


def generate_dyploma(candidate_id):
    university = random.choice(universities)
    avg_mark = round(random.uniform(3.0, 5.0), 3)
    thesis_mark = random.choices([3.0, 3.5, 4.0, 4.5, 5.0], weights=[0.1, 0.2, 0.3, 0.2, 0.15])[0]
    query = 'Create (f:FirstDegreeDiplomas {universityName: "%s", averageMark: %s, thesisMark: %s})\n RETURN ID(f)'%(university, avg_mark, thesis_mark)
    diplom_id = extract_id(driver.execute_query(query_=query))
    relation_query = get_two_way_relationship(candidate_id, diplom_id, "CANDIDATE", "FIRST_DEGREE_DIPLOMAS")
    driver.execute_query(query_=relation_query)


def generate_recrutation_exemption_document(candidate_id):
    document_type = random.choice(RecruitmentExemptionDocumentTypes)
    query = get_two_way_relationship(candidate_id, document_type, "CANDIDATE", "DOCUMENTS_TYPE")
    driver.execute_query(query_=query)


def generate_fee_exempting_document(candidate_id):
    document_type_id = random.choice(FeesExemptionDocumentTypes)
    date_of_issue = fake.date_between(start_date='-2y', end_date='today')
    document_id = fake.pystr(min_chars=6, max_chars=20)
    query = get_relationship_with_attributes(candidate_id,
                                             document_type_id,
                                             "DocumentsExemptingFromFees",
                                             '{documentId:"%s", date:date("%s")}'%(document_id, date_of_issue))
    driver.execute_query(query_=query)


def generate_candidate():
    account_id = generate_candidate_account()
    name = fake.first_name()
    surname = fake.last_name()
    id_document_number = fake.passport_number()
    document_type_id, nationality = get_document_type_with_nationality()
    pesel = None
    if nationality == "Polish":
        pesel = fake_pesel.generate()
    query = 'CREATE (candidate:Candidates {name: "%s", surname: "%s", id_document_number: "%s", pesel: "%s" })\n RETURN ID(candidate)' % (name, surname, id_document_number, pesel)
    candidate_id = extract_id(driver.execute_query(query_=query))

    generate_recruitment_applications(candidate_id)
    driver.execute_query(query_=get_two_way_relationship(account_id, candidate_id, "ACCOUNT", "CANDIDATE"))

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
        year = random.choice([2017, 2018, 2019, 2020, 2021, 2022, 2023])
        round = random.choice(["FIRST", "SECOND", "THIRD"])
        major = random.choice(Majors)
        query = 'CREATE (recruitment_application: RecruitmentApplications {year: %s, round: "%s"})\n RETURN ID(recruitment_application)'%(year, round)
        application_id = driver.execute_query(query_=query)
        driver.execute_query(query_=
                             get_two_way_relationship(application_id, major, "RECRUITMENT_APPLICATIONS", "MAJORS"))
        driver.execute_query(query_=
                             get_two_way_relationship(application_id, candidate_id, "RECRUITMENT_APPLICATIONS", "CANDIDATE"))


def generate_worker_account():
    login = fake.unique.pystr_format(string_format='prac_pwr??????', letters='1234567890')
    password = fake.password()
    query = 'CREATE (account: Accounts {login: "%s", password: "%s"})\n RETURN ID(account)'%(login, password)
    return extract_id(driver.execute_query(query_=query))

workers = []

def generate_worker():
    name = fake.first_name()
    surname = fake.last_name()
    phone_number = fake.phone_number()
    mail = fake.email()
    account_id = generate_worker_account()
    worker_id = extract_id(driver.execute_query(
        query_='CREATE (recruitment_worker: RecruitmentWorkers {name: "%s", surname: "%s", phone_number: "%s", mail: "%s"})\n RETURN ID(recruitment_worker)'%(name, surname, phone_number, mail))
    )
    driver.execute_query(query_=get_two_way_relationship(
        worker_id, account_id, "RECRUITMENT_WORKERS", "ACCOUNTS")
    )
    workers.append(worker_id)

def generate_worker_for_major():
    for major in Majors:
        worker_number = random.randint(1, 5)
        workers_for_major = random.choices(workers, k=worker_number)
        for worker in workers_for_major:
            driver.execute_query(query_=get_two_way_relationship(
                worker, major, "RECRUITMENT_WORKERS", "MAJORS")
            )


for i in range(2):
    if i % 20 == 0:
        print("WORKER added")
    generate_worker()

generate_worker_for_major()

for i in range(20000):
    if i % 20 == 0:
        print("CANDIDATE added")
    generate_candidate()
