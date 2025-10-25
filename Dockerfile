
#FROM node:20-alpine
 FROM node:14-alpine


WORKDIR /usr/src/app

COPY package.json ./

COPY . .

EXPOSE 3000:3000

CMD ["node", "server.js"]
