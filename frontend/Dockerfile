# Start with a Node.js image that is version 20 or higher
# Use a specific version to ensure consistent builds
FROM node:20-alpine

WORKDIR /app

COPY package.json yarn.lock ./

RUN yarn install

COPY . .

RUN yarn build

EXPOSE 3000

CMD ["yarn", "start"]