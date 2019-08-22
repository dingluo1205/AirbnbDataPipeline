CREATE TABLE IF NOT EXISTS time (
date_time TIMESTAMP NOT NULL, 
day int,
week int, 
month int, 
year int,
dayofweek int,
CONSTRAINT date_pkey PRIMARY KEY (date_time)
);

CREATE TABLE IF NOT EXISTS review (
listing_id BIGINT,
reviewer_id int,
date_time TIMESTAMP, 
comments VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS listing (
listing_id BIGINT NOT NULL ,
name VARCHAR(256),
host_id int,
neighbourhood VARCHAR(256),
room_type VARCHAR(256),
price float8,
latitude float8,
longitude float8,
minimum_nights int,
availability_365 int,
host_name VARCHAR(256),
CONSTRAINT listing_pkey PRIMARY KEY (listing_id)
);

CREATE TABLE IF NOT EXISTS reviewer (
reviewer_id int,
reviewer_name VARCHAR(256),
CONSTRAINT reviewer_pkey PRIMARY KEY (reviewer_id)
);

CREATE TABLE IF NOT EXISTS calendar (
listing_id BIGINT,
date_time TIMESTAMP,
available VARCHAR(256),
price float8
);

CREATE TABLE IF NOT EXISTS staging_reviews (
listing_id BIGINT,
id int,
date VARCHAR(256),
reviewer_id int,
reviewer_name VARCHAR(256),
comments VARCHAR(256)
);

CREATE TABLE IF NOT EXISTS staging_calendar (
listing_id BIGINT,
date VARCHAR(256),
available VARCHAR(256),
price VARCHAR(256),
adjusted_price VARCHAR(256),
minimum_nights int,
maximum_nights int 
);


CREATE TABLE IF NOT EXISTS staging_listings (
id BIGINT,
name VARCHAR(256),
host_id int,
host_name VARCHAR(256),
neighbourhood_group VARCHAR(256),
neighbourhood VARCHAR(256),
latitude float8,
longitude float8,
room_type VARCHAR(256),
price float8,
minimum_nights int,
number_of_reviews int,
last_review VARCHAR(256),
reviews_per_month float8,
calculated_host_listing_count int,
availability_365 int
);