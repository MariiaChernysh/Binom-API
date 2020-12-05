#!/bin/bash
#API-request to Binom ad tracker to receive a JSON with list of campaigns on the acc:
echo "curl -X COPY \
'https://jump-track.com/panel.php?page=Campaigns&status=all&group=all&traffic_source=all&date=9&timezone=+0:00&api_key=binom_api_key' \  #insert binom api key here
  -H 'cache-control: no-cache' \
  -H 'postman-token: postmen-token-here'" |bash >>NEWData  #insert postmen token here
  
#As I work with Google Cloud Shell and BigQuery, JSON needs to be formatted accordingly. BigQuery requires newline separated JSON without square brackets 
cat NEWData | tr -d [] >>Final #delete [ ].
sed 's/},{/}\n{/g' Final >>CampList.json #replace commas with newlines
rm Final NEWData #remove tempfiles

# (Optional) Afterwards I transfer JSON to GCS
gsutil cp CampList.json gs://my_folder/CampList.json

