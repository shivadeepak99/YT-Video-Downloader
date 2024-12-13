# YouTube Video Downloader

This project, **YouTube Video Downloader**, was created by **Shivadeepak**. It allows users to download YouTube videos easily



# website hosted remotely at https://ytvideodownloader-y3ra12un.b4a.run/
## Preview
![Preview of the application](images/preview.png)
## issue at remote docker space
no available space at remote docker container so the website is  not working for medium to large size videos
i.e if you are seeing error it means the space was not sufficient to store and send the file  so clone this to your localhost 
## Features
- User-friendly interface.
- Supports video and audio  merged downloads.

## Project Details
- **Creator**: Shivadeepak
- **GitHub Repository**: [YTVideoDownloader](https://github.com/shivadeepak99/YTVideoDownloader)
# uing dockerfile??
## Use the official Node.js image
FROM node:18 AS node_base

WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .

## Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ffmpeg \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

## Install the latest yt-dlp
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp \
    && chmod a+rx /usr/local/bin/yt-dlp

##Expose the application port
EXPOSE 3000

CMD ["npm", "start"]
## Requirements
- Python 3.x
- Required libraries (listed in `requirements.txt`)

## How to Run
1. Clone this repository:
   ```bash
   git clone https://github.com/shivadeepak99/YTVideoDownloader.git
### Navigate to the project directory
### Install dependencies:
### Run the program

## Contribution
 Feel free to contribute to this project by submitting issues or creating pull requests

## Created with ❤️ by Shivadeepak
