#!/bin/bash

# Set the default CORS setting
CORS_ALLOWED_ORIGINS=${CORS_ALLOWED_ORIGINS:-"http://localhost:8000"}

# Run Rasa with the CORS setting
rasa run --enable-api --cors "$CORS_ALLOWED_ORIGINS"
