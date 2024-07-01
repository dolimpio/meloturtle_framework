FROM node:20.11.1-alpine3.19

WORKDIR /meloturtle-frontend

COPY public/ /meloturtle-frontend/public

COPY src/ /meloturtle-frontend/src

COPY package.json /meloturtle-frontend/

COPY index.html /meloturtle-frontend/

COPY vite.config.js /meloturtle-frontend/

RUN npm install

RUN npm i -g serve

RUN npm run build

EXPOSE 3000

CMD [ "serve", "-s", "dist" ]