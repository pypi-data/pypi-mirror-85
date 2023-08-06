-- Virtual IP range are declared for use by cornac in `virtual_ip_ranges`
-- table. Upon creation of a HA cluster, cornac allocates an IP from one of the
-- IP range available, and registers the allocation in `virtual_ip_allocations`.

CREATE TABLE cornac.virtual_ip_ranges (
       id SERIAL PRIMARY KEY,
       -- Check for overlapping range is done in application.
       range cidr UNIQUE,
       comment TEXT
);


CREATE TABLE cornac.virtual_ip_allocations (
       id SERIAL PRIMARY KEY,
       range_id INTEGER REFERENCES cornac.virtual_ip_ranges(id) NOT NULL,
       instance_id INTEGER REFERENCES cornac.db_instances(id) NOT NULL,
       address inet UNIQUE
);
