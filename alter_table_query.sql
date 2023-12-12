CREATE TABLE "applications_history" (
  "pk_id" integer PRIMARY KEY,
  "fk_application" integer NOT NULL,
  "fk_status" varchar NOT NULL,
  "date_status_setting" timestamp NOT NULL
);

CREATE TABLE "application_status" (
  "pk_name" varchar PRIMARY KEY
);

ALTER TABLE "applications_history" ADD FOREIGN KEY ("fk_status") REFERENCES "application_status" ("pk_name") ON DELETE CASCADE;

ALTER TABLE "applications_history" ADD FOREIGN KEY ("fk_application") REFERENCES "recruitment_applications" ("pk_id") ON DELETE CASCADE;
