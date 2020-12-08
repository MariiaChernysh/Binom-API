# Binom-API-Bash
[in progress]
This project contains scripts that help to receive the data from Binom ad tracker in JSON and CSV formats. Useful info on Binom API requests can be found [here](https://docs.binom.org/api.php) and [here](https://documenter.getpostman.com/view/4002000/RVu7Dnr4). 

Although Binom is a powerful ad manager, it has number of limitations and weak points. The inability to display the dynamics of any parameters in a large timeframe is only one of them. The following scripts help to curl the available data and prapare it for further transformations. The recieved outputs can be be aggregated and enriched to be used in further analythis.

All scripts are written to be executable in Cloud Shell (GCP)
To launch script print in Shell: 
>chmod +x ScriptName.sh # make executable

>./ScriptName.sh #launch script

**Abbreviations used:**
  - GCP - Google Cloud Platform
  - GCS - Google Cloud Stotage

## CampList.sh
[Script](https://github.com/MariiaChernysh/Binom-API-Bash/blob/main/CampList.sh) returns the list of ad campaigns running in Binom in JSON format

## DailyGeoJSON.sh
This [script](https://github.com/MariiaChernysh/Binom-API-Bash/blob/main/DailyGeoJSON.sh) returns JSON file. It contains data on how traffic was distributed by geos for every campaign in a specific date. This way one can see "Live" data. 
Here I should explain what Live data in this case is. Binom puts Late Sales not in the date they were made, but to the Lead|Registration date. So you won't see reliable historical data in your tracker. On the contrary, every day the manager will see different KPI on every day that campaigns were running. This script daily scrapes the data for the specific date(e.g. yesterday) and saves it in GCS. This way saving the data on the daily basis will create a dataset with only Live data. 

## DailyGeoCSV.sh
This [script]() does exactly same job as DailyGeoJSON.sh but produces csv output. Because of Binoms' json stucture(listing objects instead of nesting data) and data enrichment,  csv transformation is part of a parsing loop.
