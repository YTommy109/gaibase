-- migrate:up

CREATE TABLE IF NOT EXISTS workspaces (
  id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  title varchar(255) NOT NULL,
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  disabled_at timestamp with time zone
);

CREATE OR REPLACE VIEW workspaces_active AS
  SELECT
    id,
    title,
    created_at,
    updated_at
  FROM workspaces
  WHERE disabled_at IS NULL;

-- migrate:down

DROP VIEW IF EXISTS workspaces_active;
DROP TABLE IF EXISTS workspaces;
