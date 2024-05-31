# Dockerfile
FROM rasa/rasa:latest

# Set environment variables
ENV RASA_ENVIRONMENT="production"

# Copy project files
COPY . /app

# Set the working directory
WORKDIR /app

# Install custom dependencies
RUN pip install -r requirements.txt

# Run Rasa server
CMD ["run", "-m", "models", "--enable-api", "--cors", "*"]
