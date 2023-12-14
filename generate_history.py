import random
from datetime import timedelta, datetime

import psycopg2 as pg
from faker import Faker

fake = Faker()

INSERT_STATUS_QUERY = '''
            INSERT INTO applications_history (fk_application, fk_status, date_status_setting)
            VALUES (%s, %s, %s)
        '''

conn = pg.connect("dbname=recruitment user=postgres port=5432 password=admin")
cur = conn.cursor()

application_statuses = ["In progress", "Examined", "Unpaid", "Approved", "Rejected"]
for status in application_statuses:
    cur.execute('''
        INSERT INTO application_status (pk_name)
        VALUES (%s)
    ''', (status,))

cur.execute("SELECT pk_id,year FROM recruitment_applications")
applications = cur.fetchall()


# Define function to generate fake date within a range, with a maximum interval of 3 months
def generate_fake_date_within_3_months(start_date, end_date):
    max_interval = timedelta(days=90)  # 3 months
    return fake.date_time_between_dates(
        datetime(start_date, 1, 1),
        min(datetime(end_date, 12, 31), datetime(start_date, 1, 1) + max_interval)
    )


# Insert fake data into applications_history
for application_id, year in applications:

    in_progress_date = generate_fake_date_within_3_months(year, year + 1)
    statuses = ["In progress"]
    last_status_date = in_progress_date
    cur.execute(INSERT_STATUS_QUERY, (application_id, "In progress", in_progress_date))

    examined = random.choices([True, False], weights=[0.2, 0.8])[0]
    if year != 2023 or examined:
        last_status_date = in_progress_date + timedelta(days=random.randint(1, 30 * 3))
        cur.execute(INSERT_STATUS_QUERY,
                    (application_id, "Examined", last_status_date))
        statuses.append("Examined")

    # "Unpaid" is optional
    unpaid = random.choices([True, False], weights=[0.2, 0.8])[0]
    if unpaid:
        last_status_date = last_status_date + timedelta(days=random.randint(1, 30 * 3))
        cur.execute(INSERT_STATUS_QUERY,
                    (application_id, "Unpaid", last_status_date))

    if (year == 2023 and random.choice([True, False]) and "Examined" in statuses) or year != 2023:
        status = random.choice(["Approved", "Rejected"])
        last_status_date = last_status_date + timedelta(days=random.randint(1, 30 * 3))
        cur.execute(INSERT_STATUS_QUERY,
                    (application_id, status, last_status_date))

# Commit the changes
conn.commit()
