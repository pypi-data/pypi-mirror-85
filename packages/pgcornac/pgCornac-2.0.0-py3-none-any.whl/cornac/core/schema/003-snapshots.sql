CREATE TYPE cornac."db_snapshot_status" AS ENUM (
  -- Keep it sync with cornac/core/model.py.
  'available',
  'creating',
  'deleted',
  'failed'
);

CREATE TYPE cornac."db_snapshot_type" AS ENUM (
  -- Keep it sync with cornac/core/model.py.
  'automated',
  'manual'
);

CREATE TABLE cornac.db_snapshots (
  id BIGSERIAL PRIMARY KEY,
  identifier TEXT UNIQUE,
  status cornac.db_snapshot_status NOT NULL,
  status_message TEXT,
  instance_id INTEGER REFERENCES cornac.db_instances(id),
  "type" cornac.db_snapshot_type NOT NULL,
  "data" JSONb,
  "iaas_data" JSONb,
  "operator_data" JSONb
);

ALTER TABLE cornac.db_instances
  ADD COLUMN IF NOT EXISTS recovery_token TEXT UNIQUE;

CREATE INDEX ON cornac.db_snapshots(instance_id);
