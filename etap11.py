from neo4j import GraphDatabase

URI = "neo4j+s://f53af4cc.databases.neo4j.io"
AUTH = ("neo4j", "1Ob6tEcO0946BsXr9ggRQmVe6834TS68qJikhcTUWJM")

queries = ['CREATE (major:Majors {name: "Applied Computer Science", description: "The field allows students to develop new skills and acquire new knowledge on the broadly understood computer science and its various implementations in solving business or technical problems or in the computer game sector. Applied computer science is supplemented with training in physics and mathematics, basic entrepreneurship courses, as well as in social and professional issues in computer science. Much emphasis is also placed on soft skills, such as presentation skills and teamwork skills.", number_of_places: 170})',
           'CREATE (course: Courses {code: "W04IST-SI0815G", name: "Database Design", description: "A class focusing on the design of relational and non-relational databases"})',
           'CREATE (threshold: Thresholds {recrutation_year: 2023, points: 470.05, round_number: 1})',
           'CREATE (recruitment_worker: Recruitment_workers {name: "Stefan", surname: "Kowalski", phone_number: "135-123-312", mail: "stefan.kowalski@pracownik.pwr.edu.pl"})',
           'CREATE (account: Accounts {login: "pwr354275", password: "38thfj3d"})',
           'CREATE (recruitment_application: Recruitment_applications {year: 2023, round: 1})',
           'CREATE (application_status: Application_status {name: "APPROVED"})',
           'CREATE (:Major_algorithms {name: "algorithm for IT direction"})',
           'CREATE (:Subjects {name: "Mathematics"})',
           'CREATE (:Departments {code: "W04n", name: "Faculty of Information and Communication Technology", description: "Information has always been a precious commodity. However, it has never been so widely available as it is now. Almost anywhere in the world. We have become an information society that needs, and is also able to, make better and better use of information systems and telecommunications services. They allow not only long-distance communication, but also the sending of information from any place on earth with the use of mobile devices. Therefore, modern society makes use of systems which allow the storage, transmission and processing of information. The efficiency of our societies depends on the safe and reliable operation of these systems. The challenge is to expand the scope of resources, ensuring access to verifiable and correct information."})',
           'MATCH (m:Majors {name: "Applied Computer Science"})\nMATCH (d:Departments {code: "W04n"}) \nCREATE (m)-[:MAJOR_IS_IN_DEPARTMENT]->(d);',
           'MATCH (m:Majors {name: "Applied Computer Science"})\nMATCH (d:Departments {code: "W04n"}) \nCREATE (d)-[:DEPARTMENT_WITH_MAJOR]->(m);',
           'MATCH (m:Majors {name: "Applied Computer Science"})\nMATCH (c:Courses {name: "Database Design"}) \nCREATE (c)-[:COURSE_MAJOR]->(m);',
           'MATCH (m:Majors {name: "Applied Computer Science"})\nMATCH (c:Courses {name: "Database Design"}) \nCREATE (m)-[:MAJOR_COURSE]->(c);',
           'MATCH (m:Majors {name: "Applied Computer Science"})\nMATCH (t:Thresholds {points: 470.05}) \nCREATE (m)-[:MAJOR_THRESHOLDS]->(t);',
           'MATCH (m:Majors {name: "Applied Computer Science"})\nMATCH (r:Recruitment_workers {name: "Stefan"}) \nCREATE (m)-[:MAJOR_RECRUITMENT_WORKER]->(r);',
           'MATCH (m:Majors {name: "Applied Computer Science"})\nMATCH (r:Recruitment_workers {name: "Stefan"}) \nCREATE (r)-[:RECRUITMENT_WORKER_MAJOR]->(m);',
           'MATCH (a:Accounts {login: "pwr354275"})\nMATCH (r:Recruitment_workers {name: "Stefan"}) \nCREATE (a)-[:ACCOUNT_RECRUITMENT_WORKER]->(r);',
           'MATCH (a:Accounts {login: "pwr354275"})\nMATCH (r:Recruitment_workers {name: "Stefan"}) \nCREATE (r)-[:RECRUITMENT_WORKER_ACCOUNTS]->(a);',
           'MATCH (a:Majors {name: "Applied Computer Science"}) \nMATCH  (ra: Recruitment_applications) \nCREATE (a)-[:MAJOR_RECRUITMENT_APPLICATION]->(ra);',
           'MATCH (a:Majors {name: "Applied Computer Science"}) \nMATCH  (ra: Recruitment_applications) \nCREATE (ra)-[:RECRUITMENT_APPLICATION_MAJOR]->(a);',
           'MATCH (a:Application_status {name: "APPROVED"}) \nMATCH  (ra: Recruitment_application {year: 2023}) \nCREATE (ra)-[:RECRUITMENT_APPLICATION_APPLICATION_STATUS{data:date("2023-06-10")}]->(a);',
           'MATCH (a:Majors {name: "Applied Computer Science"}) \nMATCH  (ma: Major_algorithms {name: "algorithm for IT direction"}) \nCREATE (a)-[:MAJOR_MAJOR_ALGORITHMS]->(ma);',
           'MATCH (a:Majors {name: "Applied Computer Science"}) \nMATCH  (ma: Major_algorithms {name: "algorithm for IT direction"}) \nCREATE (ma)-[:MAJOR_ALGORITHMS_MAJOR]->(a);',
           'CREATE (candidate:Candidates {name: "Jan", surname: "Kowalski", id_document_number: "CHB1234567", pesel: "02215276356" })',
           'Match (c:Candidates)\nCreate (c)-[:DOCUMENTS_EXEMPTING_FROM_RECRUITMENT {documentId:"JYVwiu9726497", date:date("2019-06-10")}]->(r:RecruitmentExemptionDocumentTypes {name: "Studium Talent"})',
           'Match (c:Candidates)\nCreate (c)-[:CANDIDATE_NATIONALITY]->(n:Nationality {name: "Polish", studies_fee_free:true})\nCreate (n)-[:NATIONALITY_CANDIDATE]->(c)',
           'Match (c:Candidates)\nCreate (c)-[:DOCUMENTS_EXEMPTING_FROM_FEES {documentId:"JYVwiu9726gw2", date:date("2019-06-10")}]->(t:FeesExemptionDocumentTypes {name: "Karta Polaka"})',
           'Match (c:Candidates)\nCreate (id:IdDocumentTypes {name:"Dowód osobisty"})-[:ID_DOCUMENT_TYPE_CANDIDATE]->(c)\nCreate (c)-[:CANDIDATE_ID_DUCUMENT_TYPE]->(id)',
           'Match (c:Candidates)\nCreate (f:FirstDegreeDiplomas {universityName: "Politechnika Wrocławska", averageMark: 4.5, thesisMark: 5.0})-[:FIRST_DEGREE_DIPLOMA_CANDIDATE]->(c)\nCreate (c)-[:CANDIDATE_FIRST_DEGREE_DIPLOMA]->(f)',
           'Match (c:Candidates)\nCreate (e:Exams {documentId: "37o83gsteyz", date: date("2019-06-10")})-[:EXAM_CANDIDATE]->(c)\nCreate (c)-[:CANDIDATE_EXAM]->(e)',
           'Match (e:Exams)\nCreate (e)-[:EXAM_EXAM_TYPE]->(et:ExamType {name: "Nowa Matura", minimumPointsScore: 0, maximumPointsScore: 100, multiplier: 1.0})\nCreate (et)-[:EXAM_TYPE_EXAM]->(e)',
           'Match (c:Candidates)\nMatch (a:Accounts)\nCREATE (c)-[:CANDIDATE_ACCOUNT]->(a)\nCREATE (a)-[:ACCOUNT_CANDIDATE]->(c)',
           'Match (c:Candidates)\nMatch (r:Recruitment_applications)\nCREATE (r)-[:RECRUITMENT_APPLICATION_CANDIDATE]->(c)\nCREATE (c)-[:CANDIDATE_RECRUITMENT_APPLICATION]->(r)',
           'Match (e:Exams)\nMatch (s:Subjects)\nCreate (e)-[:SUBJECTS_RESULTS {points: 89}]->(s)',
           'Match (a:Application_status)\nMatch (ra:Recruitment_applications)\nCreate (ra)-[:APPLICATION_HISTORY {date: date("2023-11-12")}]->(a)',
           'MATCH (ma:Major_algorithms)\nMATCH (s:Subjects)\nCREATE (ma)-[:SUBJECTS_MENTIONED_IN_ALGORITHM {factor: 2.5}]->(s)']

with GraphDatabase.driver(URI, auth=AUTH) as driver:
    driver.verify_connectivity()
    for query in queries:
        driver.execute_query(
            query_=query,
            database_='neo4j'
        )
