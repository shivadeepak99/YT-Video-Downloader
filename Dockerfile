# Use the official Node.js image
FROM node:18 AS node_base

WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ffmpeg \
    python3 \
    python3-pip \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install the latest yt-dlp
RUN curl -L https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp -o /usr/local/bin/yt-dlp \
    && chmod a+rx /usr/local/bin/yt-dlp

# Expose the application port
EXPOSE 3000

CMD ["npm", "start"]
