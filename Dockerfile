# Gunakan base image Python
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements dan install dependency
COPY board/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy seluruh project ke dalam container
COPY . /app

# Expose port Flask
EXPOSE 5000

# Jalankan aplikasi Flask
CMD ["python", "board/app.py"]
