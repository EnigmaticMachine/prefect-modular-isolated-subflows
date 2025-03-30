FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

EXPOSE 4200

# Set the default command to run your flow deployment script.
CMD ["tail", "-f", "/dev/null"]
