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

# Install using piwheels (precompiled!)
RUN pip install -i https://www.piwheels.org/simple \
    numpy==1.21.4 \
    python-periphery \
    wiringpi

# Create 'pi' user and app directory
RUN useradd -m -s /bin/bash pi
USER pi
WORKDIR /home/pi

# Clone GrovePi and copy only grovepi.py
RUN git clone https://github.com/DexterInd/GrovePi.git && \
    mkdir -p /home/pi/app && \
    cp GrovePi/Software/Python/grovepi.py /home/pi/app/

# (Optional) Install RFR_Tools
RUN git clone https://github.com/DexterInd/RFR_Tools.git && \
    cp RFR_Tools/miscellaneous/di_i2c.py /home/pi/app/ && \
    cp RFR_Tools/miscellaneous/di_mutex.py /home/pi/app/

# Copy your app script
WORKDIR /home/pi/app
COPY app.py .

USER root

# Run the script
CMD ["python3", "-u", "app.py"]
