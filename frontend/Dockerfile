# ---- Build stage ----
FROM node:18 AS build

WORKDIR /app

# Copy dependencies
COPY package*.json ./

# Install deps
RUN npm ci

# Copy full source
COPY . .

# Build Vite for production
RUN npm run build

# ---- Runtime stage ----
FROM node:18-slim AS runtime

WORKDIR /app

# Install static server
RUN npm install -g serve

# Copy dist from build stage
COPY --from=build /app/dist ./dist

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]
