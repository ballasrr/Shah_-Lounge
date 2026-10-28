# Сайт: Nuxt собирается в статику, nginx её отдаёт и передаёт /api в бэкенд.

FROM node:22-slim AS build
WORKDIR /app
COPY package.json package-lock.json .nuxtrc ./
COPY nuxt.config.ts tsconfig.json ./
COPY app ./app
COPY public ./public
RUN npm ci --no-audit --no-fund
# адрес сайта для canonical, sitemap и превью ссылок
ARG NUXT_SITE_URL=http://localhost:8080
ENV NUXT_SITE_URL=$NUXT_SITE_URL
RUN npm run generate

FROM nginx:1.27-alpine
COPY docker/nginx.conf /etc/nginx/conf.d/default.conf
COPY --from=build /app/.output/public /usr/share/nginx/html
