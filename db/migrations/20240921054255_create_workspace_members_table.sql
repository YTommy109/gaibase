-- migrate:up

CREATE TYPE member_role AS ENUM ('manager', 'leader', 'member');

CREATE TABLE IF NOT EXISTS workspace_members (
  id uuid NOT NULL DEFAULT gen_random_uuid() PRIMARY KEY,
  account_id uuid NOT NULL REFERENCES accounts(id),
  workspace_id uuid NOT NULL REFERENCES workspaces(id),
  role member_role NOT NULL DEFAULT 'member',
  created_at timestamp with time zone NOT NULL DEFAULT now(),
  updated_at timestamp with time zone NOT NULL DEFAULT now(),
  disabled_at timestamp with time zone
);

CREATE OR REPLACE VIEW workspace_members_active AS
  SELECT
    id,
    account_id,
    workspace_id,
    role,
    created_at,
    updated_at
  FROM workspace_members
  WHERE disabled_at IS NULL;

-- migrate:down

DROP VIEW IF EXISTS workspace_members_active;
DROP TABLE IF EXISTS workspace_members;
DROP TYPE IF EXISTS member_role;
