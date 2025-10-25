
FROM node:20-alpine
  
WORKDIR /usr/src/app

COPY package.json ./

COPY . .

EXPOSE 3000:3000

CMD ["node", "server.js"]
