# Base image
FROM python:3.9-slim



# Set work directory

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


RUN mkdir usr/JonasJones && \
    chown root:root usr/JonasJones && \
    chmod 1777 usr/JonasJones


RUN useradd -m usr/JonasJones && \
    chown -R usr/JonasJones:usr/JonasJones /home/usr/JonasJones


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh


WORKDIR /app
COPY . /app

EXPOSE 8000

RUN pip install --no-cache-dir -r requirements.txt

# Command to run the application
CMD ["/entrypoint.sh"]
