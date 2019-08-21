# AirbnbDataPipeline
Build an end-to-end data pipeline for Airbnb review and listing data 

## Section 1: Scope the Project and Gather Data
Since 2008, guests and hosts have used Airbnb to travel in a more unique, personalized way. Inside Airbnb (http://insideairbnb.com/about.html) is an independent, non-commercial set of tools and data that allows you to explore how Airbnb is really being used in cities around the world.

The scope of this project is to gather data from this open data source, load them into S3 bucket, and transform them to a well defined schema that analyts and scientist can use for the analysis purpose. As the Inside Airbnb provides data for more than 20 major cities,and for the past three years, in this project, I only covered 3 major cities (Boston, New York, and Seattle). 

Here are some of the questions that can be answered through this new data warehouse - 

1. "How many listings are in my neighbourhood and where are they?"
2. "What is the average minimum nights stay in my neighbourhood?"
3. "Which hosts are running a business with multiple listings and where are they?"

I will provide detailed query examples later in the following sections. 

## Section 2: Explore and Assess the Data
There are two types of data in this project. One is csv/csv.gz, and another is geojson. 

### Files 
There are mainly four files - calendar, reviews, listings, and neighbourhood. The neighbourhood is a geojson file. It can be used for visualization purpose.

Calendar - including listing id and the price and availability for that day

Reviews - including unique id for each reviewer and detailed comments

Listings - including full descriptions and average review score for each listing 

The files are stored per city and per month. So I stored them separately in my S3 bucket, paritioned on month. 

## Section 3: Define the Data Model
In this project, I used star schema to deisgn the data model. Please refer to the design below - 

![Data Model](/data%20diagram.png)

## Section 4: Run ETL to Model the Data in Airflow 
The reason why I chose airflow is that the whole end-to-end data ingestion needs to be done at monthly basis. Every month, Inside Airbnb will provide new month's data in their website. In this way, the jobs need to run at once in a month, and if it fails, backfill will be needed. I've configured all these settings in the DAG config. However, if the data is increased by 100x (for example, summer vacation at Boston when a lot of international students come visit), the 

* The DAG does not have dependencies on past runs
* On failure, the task are retried 3 times
* Retries happen every 5 minutes
* Catchup is turned off

Please refer to the graph view follows the flow shown in the image below - 

## Section 5: Sample analysis queries 

## Section 6: Limitations 
The data was increased by 100x.
