FROM node:20-bullseye

WORKDIR /opt/app

COPY . .

RUN npm i

ENTRYPOINT ["npm", "start"]
