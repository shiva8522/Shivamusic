# Use Python 3.9 Image
FROM python:3.9

# Set Environment Variables
ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port & run the application
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "mymusicapp.wsgi:application"]
