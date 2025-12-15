FROM node:25.2.1-alpine3.22 AS build
WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
CMD ["npm", "run", "dev"]
