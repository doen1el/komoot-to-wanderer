FROM python:3.11-slim

WORKDIR /app

# Update and clean the apt cache
RUN apt-get update && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the files
COPY ./main.py ./
COPY ./helper ./helper
COPY ./requirements.txt ./

# Install the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Run the application
CMD ["python", "main.py"]
