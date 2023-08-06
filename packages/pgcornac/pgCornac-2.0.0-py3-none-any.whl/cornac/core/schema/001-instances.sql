-- cf. https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/Overview.DBInstance.Status.html
CREATE TYPE cornac."db_instance_status" AS ENUM (
  'available',
  'backing-up',
  -- 'backtracking',  Only for Aurora.
  -- 'configuring-enhanced-monitoring',  Only for MySQL.
  -- 'configuring-iam-database-auth',  Only on AWS.
  -- 'configuring-log-exports',  Only on AWS.
  -- 'converting-to-vpc',  Only on AWS.
  'creating',
  'deleting',
  'failed',
  -- 'inaccessible-encryption-credentials',  Only on AWS.
  'incompatible-network',
  'incompatible-option-group',
  'incompatible-parameters',
  'incompatible-restore',
  'maintenance',
  'modifying',
  -- 'moving-to-vpc',  Only on AWS.
  'rebooting',
  'renaming',
  'resetting-master-credentials',
  'restore-error',
  'starting',
  'stopped',
  'stopping',
  'storage-full',
  'storage-optimization',
  'upgrading'
);

CREATE TABLE cornac.db_instances (
  id BIGSERIAL PRIMARY KEY,
  identifier TEXT UNIQUE,
  status cornac.db_instance_status NOT NULL,
  status_message TEXT,
  recovery_token TEXT UNIQUE,
  "data" JSONb,
  iaas_data JSONb,
  operator_data JSONb
);
