-- migrate:up

CREATE TYPE system_role AS ENUM ('admin', 'user');

CREATE TABLE IF NOT EXISTS accounts (
  id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  name varchar(255) NOT NULL,
  email varchar(255) NOT NULL,
  role system_role NOT NULL DEFAULT 'user',
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  disabled_at timestamp with time zone
);

CREATE OR REPLACE VIEW accounts_active AS
  SELECT
    id,
    name,
    email,
    role,
    created_at,
    updated_at
  FROM accounts
  WHERE disabled_at IS NULL;

-- migrate:down

DROP VIEW IF EXISTS accounts_active;
DROP TABLE IF EXISTS accounts;
DROP TYPE IF EXISTS system_role;
