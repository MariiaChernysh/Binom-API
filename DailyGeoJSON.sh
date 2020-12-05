#!/bin/bash
 
date > b
echo "Enter the date you'd like to scrape"
read dt
for date in $dt
do
#Not all campaigns constantly receive traffic. To reduce API request execution time one can list campaigns numbers that should be requested. 
#The following loop runs API requests for every listed campaign consequentially and appends data to temp file
	for camp in 7 10 45 {400..500}
		do
			echo $date $camp
      #Enrich data with campaign's ids and date 
			echo '{"'id'" : "'$camp'","date":"'$date'","Countries":'>>NEWData
      #API request
			echo "curl -X COPY \
  'https://jump-track.com/panel.php?page=Stats&camps=$camp&group1=19&group2=1&group3=1&date=12&date_s=$date&date_e=$date&timezone=%200:00&api_key=api_key_here' \ #insert api key here
  -H 'cache-control: no-cache' \
  -H 'postman-token: postman-token-here'" |bash >>NEWData #insert postman token here
  			echo '}' >>NEWData
		done
	wait
done 
#Process data as json with jq 
cat NEWData | jq -c '.'>Final
#Some campaigns have a string "no clicks" instead of data. Exclude them from the final file with grep. 
grep "level" Final >Live.json

#(Optional). Transfer the file from Shell environment to GCS 
gsutil cp Live.json gs://my_folder/Live.json
#(Optional). Append file to dataset with privious dates
gsutil compose gs://my_folder/LiveData.json gs://my_folder/Live.json \gs://my_folder/LiveData.json 
#Clean Shell environment from temp files
rm Final NEWData Live.json
date >>b 
cat b
