FROM arm32v7/python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    curl \
    i2c-tools \
    build-essential \
    libatlas-base-dev \
    python3-pip \
    python3-setuptools \
    && rm -rf /var/lib/apt/lists/*

# Install necessary Python packages
RUN pip install -i https://www.piwheels.org/simple \
    numpy==1.21.4 \
    python-periphery \
    wiringpi \
    flask \
    requests

# Set working directory
WORKDIR /home/pi/app

# Clone required repositories and extract needed files
RUN git clone https://github.com/DexterInd/GrovePi.git && \
    git clone https://github.com/DexterInd/RFR_Tools.git && \
    cp GrovePi/Software/Python/grovepi.py \
        RFR_Tools/miscellaneous/di_i2c.py \
        RFR_Tools/miscellaneous/di_mutex.py . && \
    rm -rf GrovePi RFR_Tools

# Copy your application file(s) from host
COPY . .

# Run the script
CMD ["python3", "-u", "app.py"]
