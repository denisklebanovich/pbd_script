import random

from generate import cur, fake

application_status = {
    "In progress": 0,
    "Unpaid": 1,
    "Examined": 2,
    "Approved": 3,
    "Rejected": 3
}

cur.execute("SELECT pk_id FROM recruitment_applications")
application_ids = cur.fetchall()


for application_id in existing_application_ids:
    # Ensure the first status is always "In progress"
    status_sequence = ["In progress"]

    # Some applications may be examined
    if random.choice([True, False]):
        status_sequence.append("Examined")

        # Some applications may have an unpaid status
        if random.choice([True, False]):
            status_sequence.append("Unpaid")

            # If examined, some applications may be approved or rejected
            if "Examined" in status_sequence:
                decision = random.choice(["Approved", "Rejected"])
                status_sequence.append(decision)

    date = fake.date_time_between(start_date="-5y", end_date="now")
    # Loop through the status sequence for each application
    for j, status in enumerate(status_sequence):
        # Generate random timestamp for date_status_setting (replace with your logic)
        random_days = random.randint(1, 5)
        date = date + random_days

        # Insert into applications_history
        cur.execute('''
            INSERT INTO applications_history (fk_application, fk_status, date_status_setting)
            VALUES (%s, %s, %s)
        ''', (application_id, status, date_setting))
