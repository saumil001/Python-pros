# -*- coding: utf-8 -*-
# I used beautiful soup for downloding images from web
# Program automatic open all links from the file and download all images which 
# were appeared on the webpage --> save to your current folder where your python 
# script is located.
# I used some marathon website for better use this program 
# their are lots of images.


# import the necessary packages
from selenium import webdriver
import datetime
import time
import argparse
import os
import requests
import urllib.request
import random
import bs4

url = "https://www.myracephotos.in/Event-Photos/2019/Coimbatore-Marathon-2019"

# Extract the album name
album_name = url.split('/')[-2]

# Define Chrome options to open the window in maximized mode
options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

# Initialize the Chrome webdriver and open the URL
driver = webdriver.Chrome(chrome_options=options)
driver.get(url)

# Define a pause time in between scrolls
pause_time = 2

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

# Record the starting time
start = datetime.datetime.now()

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # wait to load page
    time.sleep(pause_time)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height: # which means end of page
        break
    # update the last height
    last_height = new_height

# Record the end time, then calculate and print the total time
end = datetime.datetime.now()
delta = end-start
print("[INFO] Total time taken to scroll till the end {}".format(delta))

# Extract all anchor tags
link_tags = driver.find_elements_by_tag_name('a')

# Create an emply list to hold all the urls for the images
hrefs = []

# Extract the urls of only the images from each of the tag WebElements
for tag in link_tags:
    if "sm-tile-content" not in tag.get_attribute('class'):
        continue
    hrefs.append(tag.get_attribute('href'))

# Download all images and scoll down with automatically changes name of file.
for href in hrefs:
    image_name = "001.jpeg"
#    images = []
    driver.get(href)
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # wait to load page
        time.sleep(pause_time)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height: # which means end of page
            break
        # update the last height
        last_height = new_height
#    time.sleep(5)
    images_tags = driver.find_elements_by_tag_name('img')
    images = [tag.get_attribute('src') for tag in images_tags if 'sm-image' in tag.get_attribute('class') ]
    for image in images:
        urllib.request.urlretrieve(image,image_name)
        image_name = image_name.split(".")[0][0:3] + str(random.randint(0,50)) + '.jpg'

dir_name = 'img_pg_links'
if not os.path.exists(dir_name):
    try:
        os.mkdir(dir_name)
    except OSError:
        print ("[INFO] Creation of the directory {} failed".format(os.path.abspath(dir_name)))
    else:
        print ("[INFO] Successfully created the directory {} ".format(os.path.abspath(dir_name)))

# Write the links to the image pages to a file
f = open("{}/{}.csv".format(dir_name, album_name),'w')
f.write(",\n".join(hrefs))
print ("[INFO] Successfully created the file {}.csv with {} links".format(album_name, len(hrefs)))
