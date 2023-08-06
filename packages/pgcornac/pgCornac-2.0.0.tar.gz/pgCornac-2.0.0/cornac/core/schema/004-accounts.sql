CREATE TABLE IF NOT EXISTS cornac.accounts (
  id BIGSERIAL PRIMARY KEY,
  alias TEXT UNIQUE NOT NULL,
  data jsonb DEFAULT '{}'::jsonb
);


ALTER TABLE cornac.db_instances
  ADD COLUMN IF NOT EXISTS
  account_id BIGINT REFERENCES cornac.accounts(id) NOT NULL;

ALTER TABLE cornac.db_instances
  DROP CONSTRAINT db_instances_identifier_key;

CREATE UNIQUE INDEX db_instances_unique_identifier
  ON cornac.db_instances (account_id, identifier);


ALTER TABLE cornac.db_snapshots
  ADD COLUMN IF NOT EXISTS
  account_id BIGINT REFERENCES cornac.accounts(id) NOT NULL;

ALTER TABLE cornac.db_snapshots
  DROP CONSTRAINT db_snapshots_identifier_key;

CREATE UNIQUE INDEX db_snapshots_unique_identifier
  ON cornac.db_snapshots (account_id, identifier);


CREATE TYPE cornac."identity_type" AS ENUM ('group', 'role', 'user');

CREATE TABLE cornac.identities (
  id BIGSERIAL PRIMARY KEY,
  account_id BIGINT REFERENCES cornac.accounts(id) NOT NULL,
  -- Fast access to role for group allowed to assume admin role on other
  -- account. This is the reverse of Principal.
  allowed_role_id BIGINT REFERENCES cornac.accounts(id),
  arn TEXT UNIQUE,
  type cornac.identity_type,
  name TEXT NOT NULL,
  reset_token TEXT,
  reset_edate TIMESTAMP WITH TIME ZONE,
  data jsonb,
  UNIQUE(account_id, type, name)
);

CREATE UNIQUE INDEX globally_unique_username
  ON cornac.identities (name)
  WHERE type = 'user';

CREATE UNIQUE INDEX reset_token
  ON cornac.identities (reset_token)
  WHERE reset_token IS NOT NULL;

-- Ensure only one group is allowed to assume a delegation role.
CREATE UNIQUE INDEX delegated_group
  ON cornac.identities (account_id, allowed_role_id)
  WHERE type = 'group' AND allowed_role_id IS NOT NULL;

CREATE TABLE cornac.group_memberships (
  group_id BIGINT NOT NULL REFERENCES cornac.identities(id)
    ON DELETE CASCADE,
  member_id BIGINT NOT NULL REFERENCES cornac.identities(id)
    ON DELETE CASCADE,
  PRIMARY KEY (group_id, member_id)
);

CREATE TYPE cornac."access_key_status" AS ENUM ('Active', 'Inactive');

CREATE TABLE cornac.access_keys (
  id BIGSERIAL PRIMARY KEY,
  identity_id BIGINT NOT NULL REFERENCES cornac.identities(id)
    ON DELETE CASCADE,
  access_key TEXT UNIQUE,
  status cornac.access_key_status NOT NULL,
  session_token TEXT,
  edate TIMESTAMP WITH TIME ZONE DEFAULT NULL,
  data jsonb DEFAULT '{}'::jsonb
);

CREATE INDEX access_key_auth
  ON cornac.access_keys (access_key, status, edate);

CREATE INDEX session_token_unique
  ON cornac.access_keys (session_token)
  WHERE session_token IS NOT NULL;

CREATE TYPE cornac."acl_effect" AS ENUM ('Deny', 'Allow');

CREATE TABLE cornac."acl_statements" (
  id BIGSERIAL PRIMARY KEY,
  identity_id BIGINT NOT NULL REFERENCES cornac.identities(id)
    ON DELETE CASCADE,
  "source" TEXT NOT NULL,
  "effect" cornac.acl_effect NOT NULL,
  "action" TEXT NOT NULL,
  resource TEXT NOT NULL,
  data jsonb DEFAULT '{}'::jsonb NOT NULL,
  UNIQUE(source, action, resource)
);
