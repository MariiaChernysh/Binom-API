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
Returns the list of adcampaigns rinning in Binom in JSON format
