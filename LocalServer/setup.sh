#!/bin/bash

# Directory where the docker-compose.yml is located
DOCKER_COMPOSE_DIR="/home/ubuntu/LocalServer"

# Change to the docker-compose directory
cd "$DOCKER_COMPOSE_DIR" || { echo "Directory $DOCKER_COMPOSE_DIR not found."; exit 1; }

# Create directories for certificates and configuration
mkdir -p certs

# Generate a self-signed SSL certificate
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/selfsigned.key -out certs/selfsigned.crt \
  -subj "/C=DE/ST=Germany/L=LocalServer/O=LocalServer/OU=IT/CN=localhost"

# Create the nginx.conf file
cat > nginx.conf <<EOF
events {
  worker_connections 1024;
}

http {
  server {
    listen 80;
    server_name localhost;

    location / {
      return 301 https://\$host\$request_uri;
    }
  }

  server {
    listen 443 ssl;
    server_name localhost;

    ssl_certificate /etc/nginx/certs/selfsigned.crt;
    ssl_certificate_key /etc/nginx/certs/selfsigned.key;

    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;

    location / {
      proxy_pass http://flask_server:5462;
      proxy_set_header Host \$host;
      proxy_set_header X-Real-IP \$remote_addr;
      proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
      proxy_set_header X-Forwarded-Proto \$scheme;
    }
  }
}
EOF

# Check if docker-compose.yml exists
if [ ! -f "docker-compose.yml" ]; then
  echo "docker-compose.yml not found in $DOCKER_COMPOSE_DIR"
  exit 1
fi

# Start the Docker containers
docker-compose up -d
