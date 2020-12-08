#!/bin/bash
#CSV output will contain the following columns
#-ID,Date,Country,Clicks,LP_Clicks,Leads,Cost,Revenue,FTDs 
date > b
echo "enter date"
read dt
for date in $dt
do
#Not all campaigns constantly receive traffic. To reduce API request execution time one can list campaigns numbers that should be requested. 
#The following loop runs API requests for every listed campaign consequentially, enriches data and appends it to final csv file
	for camp in 7 10 45 {400..500}
		do
			echo $date $camp
     #Enrich data with campaign's ids and date 
			echo '{"'id'" : "'$camp'","date":"'$date'","Countries":'>NEWData
     #API request
			echo "curl -X COPY \
  'https://jump-track.com/panel.php?page=Stats&camps=$camp&group1=19&group2=1&group3=1&date=12&date_s=$date&date_e=$date&timezone=%200:00&api_key=api_key_here' \  #insert api key here
  -H 'cache-control: no-cache' \
  -H 'postman-token: postman-token-here'" |bash >>NEWData #insert postman token here
  			echo '}' >>NEWData
        # Output looks smth like: {id, date, Country:[lots of columns]} 
        # Convert json to csv wsith jq (firstly parse nested data)
  			cat NEWData | jq -r '.Countries[]| [.name, .clicks, .lp_clicks, .leads, .cost, .revenue, .a_leads] | join(",")' >Output
        # As we received newline separated json, set IFS aprropriately
  			IFS=$'\n' 
        # Now as we're doing this inside of loop that parses specific campaign at the specific date, we can echo them to csv and than echo esch row of Countries data
  			for i in $(cat Output); do echo ''$camp','$date','$i''>>LiveCRs.csv; done
  			rm Output
  			wait
		done
	wait
done 
#(Optional). Transfer the file from Shell environment to GCS 
gsutil cp LiveCRs.csv gs://my_folder/LiveCRs.csv
#Clear temp files
rm Final NEWData NEWData1 Output LiveCRs.csv
date >>b 
cat b
