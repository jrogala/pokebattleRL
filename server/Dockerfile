FROM node:latest

RUN git clone https://github.com/smogon/pokemon-showdown.git pokemonShowdown && node ./pokemonShowdown/build

WORKDIR /pokemonShowdown

COPY config.js config/config.js

CMD ["node", "pokemon-showdown", "start", "--no-security"]