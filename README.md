# AirbnbDataPipeline
Build an end-to-end data pipeline for Airbnb review and listing data 

## Section 1: Scope the Project and Gather Data
Since 2008, guests and hosts have used Airbnb to travel in a more unique, personalized way. Inside Airbnb (http://insideairbnb.com/about.html) is an independent, non-commercial set of tools and data that allows you to explore how Airbnb is really being used in cities around the world.

The scope of this project is to gather data from this open data source, load them into S3 bucket, and transform them to a well defined schema that analyts and scientist can use for the analysis purpose. As the Inside Airbnb provides data for more than 20 major cities,and for the past three years, in this project, I only covered 3 major cities (Boston, New York, and Seattle). 

## Section 2: Explore and Assess the Data
There are two types of data in this project. One is csv/csv.gz, and another is geojson. 

### Files 
There are mainly three files - calendar, reviews, and listings. Listings are saved in csv file, while the other two are saved in csv gz files. 

Calendar - including listing id and the price and availability for that day

Reviews - including unique id for each reviewer and detailed comments

Listings - including full descriptions and average review score for each listing 

The files are stored per city and per month. So I stored them separately in my S3 bucket, paritioned on month and city. 

## Section 3: Define the Data Model
In this project, I used star schema to deisgn the data model. Please refer to the design below - 

![Data Model](/data%20diagram.png)

## Section 4: Run ETL to Model the Data in Airflow 
The reason why I chose airflow is that the whole end-to-end data ingestion needs to be done at monthly basis. Every month, Inside Airbnb will provide new month's data in their website. In this way, the jobs need to run at once in a month, and if it fails, backfill will be needed. I've configured all these settings in the DAG config. However, if the data is increased by 100x (for example, summer vacation at Boston when a lot of international students come visit), the number of instances of jobs running in parallel needs to be increased to 32. As for the data quality check, I have one check on data availability, and one check on table availability. 

DAG config is as follows - 
* The DAG does not have dependencies on past runs
* On failure, the task are retried 3 times
* Retries happen every 5 minutes
* Catchup is turned off

Please refer to the graph view follows the flow shown in the image below - 

## Section 5: Sample analysis queries 

Here are some of the questions that can be answered through this new data warehouse - 

1. "How many listings are in my neighbourhood and where are they?"

Sample query - 
```
select count(distinct listing_id) 
from dim_listing 
where neighbourhood = 'East Boston'
```
```
select name, latitude, longitude
from dim_listing 
where neighbourhood = 'East Boston'
```
2. "What is the average minimum nights stay in my neighbourhood?"

Sample query - 
```
select avg(minimum_nights) 
from dim_listing 
where neighbourhood = 'East Boston'
```
3. "Which hosts are running a business with multiple listings and where are they?"

Sample query - 
```
select host_id , name, count(listing_id)
from dim_listing 
group by host_id, name 
having count(listing_id) > 1 
```
4. "What is the average price of Entire home/apt in my neighbourhood on Saturday?"

Sample query - 
```
select avg(c.price) 
from dim_listing a 
join fact_calendar c on a.list_id = c.list_id
join dim_date b on c.date_time = b.date_time 
where dayofweek = 6 
and b.available = 't'
and a.room_type = 'Entire home/apt'
```

## Section 6: Limitations 
As the data is provided by Airbnb, we do not have control over what data will flow into our data warehouse. Though I designed two data quality checks, it might not be enough. Also, this dataset lacks information for detailed reviewers. So the reviewer dimension table only has name and ID. It does not have suffficient information for us to deep dive into user behavior. Same as host information. As it is not complete as of now, I did not separate them into a different dimention table. 
