FROM python:3.7-slim

RUN apt-get update

RUN apt-get install wget -y

RUN apt-get update

RUN apt-get install gnupg -y

# Installing selenium using https://nander.cc/using-selenium-within-a-docker-container
# Adding trusting keys to apt for repositories
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -

# Adding Google Chrome to the repositories
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'

# Updating apt to see and install Google Chrome
RUN apt-get -y update

# Magic happens
RUN apt-get install -y google-chrome-stable
RUN apt-get install -yqq unzip

# Download the Chrome Driver
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/94.0.4606.61/chromedriver_linux64.zip

# Unzip the Chrome Driver into /usr/local/bin directory
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set display port as an environment variable
ENV DISPLAY=:99

# RUN apt-get install tesseract-ocr
RUN pip install selenium bs4 requests webdriver-manager
RUN pip install opencv-python pytesseract

RUN apt-get install tesseract-ocr -y

# To fix Import cv2 error - https://stackoverflow.com/questions/55313610importerror-libgl-so-1-cannot-open-shared-object-file-no-such-file-or-directo
RUN apt-get update ##[edited]
RUN apt-get install ffmpeg libsm6 libxext6  -y
