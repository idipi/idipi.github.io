# Stage 1 — Build CV (Python)
FROM python:3.12-slim AS cv-builder
RUN apt-get update \
    && apt-get install -y --no-install-recommends fonts-liberation \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY tools/cv/ tools/cv/
RUN pip install --no-cache-dir -r tools/cv/requirements.txt \
    && python tools/cv/build_cv.py /app/cv.pdf

# Stage 2 — Build Astro site (Node)
FROM node:22-alpine AS site-builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
COPY --from=cv-builder /app/cv.pdf public/cv.pdf
RUN npx astro check && npx astro build && npx pagefind --site dist

# Stage 3 — Serve
FROM nginx:alpine
COPY --from=site-builder /app/dist /usr/share/nginx/html
EXPOSE 80
