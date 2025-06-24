# Use a suitable base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app


# # Upgrade pip and install dependencies
# RUN pip install --upgrade pip \
# && pip install -r requirements.txt

# Install dependencies required by transformers
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*


# Copy app and requirements
COPY . .

# Install Python dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# # Pre-download the model (important to avoid runtime errors)
# RUN python -c "from sentence_transformers import SentenceTransformer; SentenceTransformer('all-MiniLM-L6-v2')"

# Expose port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
