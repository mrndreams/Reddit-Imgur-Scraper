import praw
import re
import os
import requests
import urllib.request
import json

# Clean up
path = os.path.join("./", "imgur_links.txt")
if os.path.exists(path):
    os.remove(path)
path = os.path.join("./", "saved_posts.txt")
if os.path.exists(path):
    os.remove(path)

# Define the output folder name prefix
folder_prefix = 'imgur_downloads'

# Find the highest numbered folder
max_num = -1
for folder_name in os.listdir('.'):
    if folder_name.startswith(folder_prefix):
        folder_num = re.findall(r'\d+', folder_name)
        if folder_num:
            max_num = max(max_num, int(folder_num[0]))

# Generate the new folder name
new_folder_name = f"{folder_prefix}{max_num+1}"

# Create the new folder
os.makedirs(new_folder_name)

with open('credentials.json') as file_object:
    credentials = json.load(file_object)


# Create a Reddit instance
reddit = praw.Reddit(client_id=credentials["CLIENT_ID"],
                     client_secret=credentials["CLIENT_SECRET"],
                     username=credentials["REDDIT_USER"],
                     password=credentials["REDDIT_PASS"],
                     user_agent='Saved Imgur Scraper')

# get the first saved post of a user
saved_posts = reddit.user.me().saved(limit=None)

with open('saved_posts.txt', 'w') as f:
    # iterate over the saved posts and print the title and URL of each post
    for post in saved_posts:
        try:
            print(post.title)
            print(post.url)
            # write post title and URL to file
            f.write(post.title + '\n')
            f.write(post.url + '\n')

            # write links within post to file
            post_content = post.selftext
            urls = re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', post_content)
            if urls:
                for url in urls:
                    print(url)
                    f.write(f'{url}\n')

        except Exception:
            pass

# print a message indicating the file has been written
print('Saved posts written to saved_posts.txt')

# open the file containing the saved posts
with open('saved_posts.txt', 'r') as f:
    # read the file contents into a variable
    file_contents = f.read()

# use regular expressions to match URLs in the file contents that start with i.imgur.com
imgur_urls = re.findall(r'https?://(?:i\.)?imgur\.com/\S+', file_contents)

# count the number of imgur links
num_imgur_links = len(imgur_urls)

# print the number of imgur links
print(f'Total number of imgur links: {num_imgur_links}')

with open('imgur_links.txt', 'w') as f:
    # iterate over the saved posts and print the title and URL of the first post
    for url in imgur_urls:
        if "account" not in url:
            try:
                f.write(url + '\n')
            except Exception:
                pass

count = 0

# Open the file containing imgur links
with open('imgur_links.txt', 'r') as f:
    # iterate over each link
    for link in f:
        # Remove any leading or trailing whitespace
        link = link.strip()
        
        # Check if the link is a gallery
        if "/a/" in link or "/gallery/" in link:
            id = os.path.basename(link)
            headers = { "Authorization": 'Client-ID b2452cf6b92f46b' } # i dont know how to secure my client id 
            response = requests.request("GET", "https://api.imgur.com/3/album/" + id + "/images", headers=headers)

            images = json.loads(response.content)["data"]

            subdir = new_folder_name + "/" + os.path.basename(link)
            os.mkdir(subdir)

            for image, i in zip(images, range(len(images))):
                print(image["link"])
                file_name = os.path.join(subdir, os.path.basename(image["link"]))
                # Download the file
                try:
                    urllib.request.urlretrieve(image["link"], file_name)
                    
                    # Print a message indicating the file has been downloaded
                    print(f"{file_name} downloaded successfully to {subdir}")
                    count = count + 1
                except Exception as e:
                    print(f"Error downloading {link}: {e}")
            
        # If the link is not a gallery, assume it's an image or video
        else:
            # Build the file name
            file_name = os.path.join(new_folder_name, os.path.basename(link))
            
            # Download the file
            try:
                urllib.request.urlretrieve(link, file_name)
                
                # Print a message indicating the file has been downloaded
                print(f"{file_name} downloaded successfully")
                count = count + 1
            except Exception as e:
                print(f"Error downloading {link}: {e}")

print(f"{count} files were successfully downloaded.")

# Support for galleries is now added :)

# if len(manuals) > 0:
#     print("-------------------------------------------------------------------------------------------------------------------------")
#     print("\n !! Since this program does not support downloading imgur galleries/albums, the following links need to be backed up manually !! \n")
#     print("-------------------------------------------------------------------------------------------------------------------------")
#     for link in manuals:
#         print(link)
