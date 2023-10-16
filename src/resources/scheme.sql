CREATE TYPE "permission_enum" AS ENUM (
  'USER_CREATE',
  'USER_READ',
  'USER_UPDATE',
  'USER_DELETE'
);

CREATE TABLE "user" (
  "id" uuid PRIMARY KEY DEFAULT (uuid_generate_v4()),
  "email" text UNIQUE NOT NULL,
  "password" text,
  "position_id" uuid
);

CREATE TABLE "role_permission" (
  "user_id" uuid NOT NULL,  
  "permission" permission_enum NOT NULL,
  PRIMARY KEY ("user_id", "permission")
);

CREATE TABLE "position" (
  "id" uuid PRIMARY KEY DEFAULT (uuid_generate_v4()),
  "title" text NOT NULL
);

COMMENT ON TABLE "user" IS 'Таблица пользователей';

COMMENT ON TABLE "role_permission" IS 'Таблица допусков пользователей';

COMMENT ON TABLE "position" IS 'Таблица должностей';

ALTER TABLE "role_permission" ADD FOREIGN KEY ("user_id") REFERENCES "user" ("id") ON DELETE CASCADE;

ALTER TABLE "user" ADD FOREIGN KEY ("position_id") REFERENCES "position" ("id") ON DELETE SET NULL;
