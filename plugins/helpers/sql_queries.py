class SqlQueries:
    ### insert statement 
    review_table_insert = ("""
        INSERT INTO review (listing_id, reviewer_id, date_time, comments) (
        SELECT distinct listing_id, reviewer_id, to_timestamp(date,'YYYY-MM-DD') as date_time, comments 
        FROM staging_reviews)
    """)

    calendar_table_insert = ("""
       INSERT INTO calendar (listing_id, date_time, available, price)(
           SELECT t.listing_id, t.date_time, t.available, cast(t.price as float) FROM (
               SELECT distinct listing_id, to_timestamp(date,'YYYY-MM-DD') as date_time, available, 
                replace(split_part(price,'$',2),',','') as price 
            FROM staging_calendar ) t
       )
    """)


    reviewer_table_insert = ("""
        INSERT INTO reviewer (reviewer_id, reviewer_name)(
        SELECT distinct reviewer_id, reviewer_name
        FROM staging_reviews
        )
    """)

    listing_table_insert = ("""
        INSERT INTO listing (listing_id, name, host_id, neighbourhood, room_type, price, latitude, longitude, minimum_nights, availability_365, host_name )(
        SELECT distinct id, name, host_id, neighbourhood, room_type, cast(price as float), latitude, longitude, minimum_nights, availability_365, host_name
        FROM staging_listings
        )
    """)

    time_table_insert = ("""
        INSERT INTO time (date_time,  day, week, month, year, dayofweek)(
        SELECT date_time, extract(day from date_time), extract(week from date_time), 
               extract(month from date_time), extract(year from date_time), extract(dayofweek from date_time)
        FROM (select date_time from review UNION select date_time from calendar)d 
        )
    """)

    #### delete statements

    review_table_delete = ("""
        DELETE FROM review
    """)

    calendar_table_delete = ("""
        DELETE FROM calendar
    """)

    reviewer_table_delete = ("""
        DELETE FROM reviewer
    """)

    listing_table_delete = ("""
        DELETE FROM listing
    """)

    time_table_delete = ("""
        DELETE FROM time
    """)