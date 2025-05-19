#############################################################
#                                                           #
#                        PRODUCTION                         #
#                                                           #
#############################################################

# Étape 1 : build de l'app Next.js
FROM node:18-alpine AS builder

ARG NEXT_PUBLIC_HOSTNAME
ARG NODE_ENV

ENV NODE_ENV=${NODE_ENV:-production}
ENV NEXT_PUBLIC_HOSTNAME=${NEXT_PUBLIC_HOSTNAME:-https://localhost}

WORKDIR /app

# Copier les fichiers nécessaires
COPY package*.json ./
RUN npm install

COPY . .

# Build en mode production
RUN npm run build

# Étape 2 : image finale optimisée
FROM node:18-alpine AS runner


ARG NEXT_PUBLIC_HOSTNAME
ARG NODE_ENV

ENV NODE_ENV=${NODE_ENV:-production}
ENV NEXT_PUBLIC_HOSTNAME=${NEXT_PUBLIC_HOSTNAME:-https://localhost}


WORKDIR /app
# Copie seulement le nécessaire pour le runtime
COPY --from=builder /app/public ./public
COPY --from=builder /app/.next ./.next
COPY --from=builder /app/node_modules ./node_modules
COPY --from=builder /app/package.json ./package.json

# Exposer le port 3000
EXPOSE 4000

# Commande de démarrage
CMD ["npm", "run", "start"]

#############################################################
#                                                           #
#                             DEV                           #
#                                                           #
#############################################################

# # Image de base avec Node.js
# FROM node:18-alpine


# ARG NEXT_PUBLIC_HOSTNAME
# ARG NODE_ENV

# ENV NODE_ENV=${NODE_ENV:-production}
# ENV NEXT_PUBLIC_HOSTNAME=${NEXT_PUBLIC_HOSTNAME:-https://localhost}


# # Définir le répertoire de travail
# WORKDIR /app
# ENV NODE_ENV=development
# ENV NEXT_PUBLIC_HOSTNAME=https://localhost

# # Copier uniquement les fichiers de dépendances pour l'installation
# COPY package*.json ./

# # Installer les dépendances
# RUN npm install

# # Copier tout le reste (sera monté comme volume en dev, donc pas nécessaire mais utile si pas monté)
# COPY . .

# # Exposer le port utilisé par Next.js
# EXPOSE 4000

# # Lancer Next.js en mode dev (avec hot reload)
# CMD ["npm", "run", "dev"]

