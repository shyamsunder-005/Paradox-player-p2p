FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libboost-system-dev \
    libboost-python-dev \
    libssl-dev \
    python3-dev \
    libtorrent-rasterbar-dev \
    && apt-get clean

# Set working directory
WORKDIR /app

# Copy files and install Python packages
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy app code
COPY . .

# Expose port for Streamlit
EXPOSE 8501

# Run the app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
