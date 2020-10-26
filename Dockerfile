FROM node:14

COPY index.js indes.js
COPY package.json package.json

RUN npm install 

CMD [ "node", "index.js" ]
