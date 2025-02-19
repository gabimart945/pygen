
# Dockerfile for Frontend
FROM node:16-alpine

# Set the working directory
WORKDIR /app

# Copy package.json and package-lock.json files
COPY package*.json /app/

# Install dependencies
RUN npm install

# Copy the source code
COPY . /app

# Build the application
RUN npm run build

# Serve the application using a static file server
RUN npm install -g serve
WORKDIR /app/build
CMD ["serve", "-s", "."]
        