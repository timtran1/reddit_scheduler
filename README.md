# reddit_scheduler

Schedule posts for Reddit using a GUI.

![demo](https://i.ibb.co/TwXMjqS/rsz-11screen-shot-2021-09-09-at-031901.png)

[Docker](https://docs.docker.com/get-docker/) and [docker-compose](https://docs.docker.com/compose/install/) are required to run this app.

*Note: the scheduler is a cron job inside the Docker container, so your Docker daemon should be running 24/7 for this to work.*

*Mac and Linux only*


## Preqs
Create a Reddit app [here](https://www.reddit.com/prefs/apps). 

Save the following:
* App client Id
* App client secret
* User agent (app name)
* Reddit username
* Reddit password

[Guide on how to find your app creds](https://www.geeksforgeeks.org/how-to-get-client_id-and-client_secret-for-python-reddit-api-registration/)

## Installation
Clone the repo and fill in above information at the `.env` file
```
CLIENT_ID=dummy
CLIENT_SECRET=dummy
USER_AGENT=dummy
USERNAME=dummy
PASSWORD=dummy
```

`cd` into the folder and run the project
```shell
docker-compose up -d
```

Access the GUI at [localhost:5000](http://localhost:5000) and start writing posts!
