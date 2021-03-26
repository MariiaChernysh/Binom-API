# Pip & .bat setup for scheduling
Basic setup for pip environment can be found [here](https://www.jetbrains.com/help/pycharm/pipenv.html)

**BUT**
If you want .bat file with py program to work properly, change your PATH variable to /Scripts/python.exe. Otherwise your cmd.exe will print an error
*"Python is not recognized as an internal or external command, operable program or batch file"*.
> setx PATH "%PATH%; ...../Scripts/python.exe"

The next step(optional) is to install gsutil, gloud and google-cloud-storage via terminal
> pip install gsutil
> 
> pip install gcloud
> 
> pip install google-cloud-storage
> 
> pip install --upgrade google-cloud-storage
> 
> pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

Make sure to authorize both in gcloud & gsutil. Print in cmd.exe and follow the instructions:

>gcloud init
>
>gsutil config
>



