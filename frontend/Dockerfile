FROM node:20.14-slim

WORKDIR /app

COPY . .

COPY .env.example .env

RUN npm install

RUN npm run build

EXPOSE 4173

CMD ["npm", "run", "preview"]