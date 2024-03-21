FROM docker.io/node:lts-alpine3.19

COPY . /app
WORKDIR /app

RUN npm install && npm run build

CMD node ./build