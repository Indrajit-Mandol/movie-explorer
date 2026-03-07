# Frontend Dockerfile — multi-stage build
FROM node:20-alpine AS builder

WORKDIR /app

# Install dependencies
COPY package.json .
RUN npm install

# Copy source
COPY . .

# Run lint + type check + build
RUN npm run build

# Production server with nginx
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# Nginx config to proxy /api to backend and handle SPA routing
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
