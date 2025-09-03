# -------- Dependencies stage: install node_modules with npm --------
FROM node:20-alpine AS deps
WORKDIR /app
# Some native modules (e.g., sharp) need this on Alpine
RUN apk add --no-cache libc6-compat python3 make g++
# Install deps using lockfile for reproducible builds
COPY package.json package-lock.json ./
RUN npm ci --legacy-peer-deps

# -------- Build stage: compile Next.js (standalone) --------
FROM node:20-alpine AS builder
WORKDIR /app
ENV NEXT_TELEMETRY_DISABLED=1

# Bring node_modules and app source
COPY --from=deps /app/node_modules ./node_modules
COPY . .

# Build your app
RUN npm run build

# -------- Runtime stage: minimal image to run the server --------
FROM node:20-alpine AS runner
WORKDIR /app

ENV NODE_ENV=production

COPY --from=builder /app/.next ./.next
COPY --from=builder /app/public ./public
COPY --from=builder /app/package.json ./package.json
COPY --from=deps /app/node_modules ./node_modules

EXPOSE 3000

CMD ["npm", "start"]
