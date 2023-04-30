# Reddit Imgur Scraper
This basic script uses the Reddit API to go through your **saved posts** and download any images/videos that are hosted on imgur
* **!! This script currently is unable to download imgur galleries/albums, but provides links to all of these at the end of the program for manual backup !!**

## Setup ##
First go to https://www.reddit.com/prefs/apps and create an app

![image](https://user-images.githubusercontent.com/89144623/235378724-e4e65518-2d15-48f9-a6cb-52803209e904.png)

**!! Make sure to select script !!** 

Enter in anything for all other fields

Once made, write down the client ID and client secret

![image](https://user-images.githubusercontent.com/89144623/235378869-ec2e5f8f-bd99-46ea-b0e5-9b89bef1aaed.png)

Once completed you can move onto preparing and running the script

## Installation and prep ##

Clone or download the repo

Open a terminal in the folder and install the requirements

`pip install -r requirements.txt`

To complete the preparation, open credentials.json and input the client id and client secret from earlier, as well as your reddit username and password. 

**!! The account you wish to save from must be the same as the one you created the bot on earlier !!**

![image](https://user-images.githubusercontent.com/89144623/235379095-e19c0d29-a279-4c9b-8135-95fc2fb3b3ae.png)

## Running the script ##

Finally, run `python main.py` to start the saving process

The script will create a unique folder in the directory where it will save all images/videos 

The script will additionally create 2 text files containing all imgur links from your reddit saved as well as all of your saved posts + titles in case they are of use to you






