FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory inside container
WORKDIR /app

# Copy requirements and install
COPY apps/backend/requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt

# Copy backend code (everything in this folder)
COPY apps/backend .

# Copy local package from one level above
COPY ./package /app/Package
RUN pip install -e /app/Package

# Set PYTHONPATH so FastAPI and local imports work
ENV PYTHONPATH=/app

# Expose FastAPI dev port
EXPOSE 8000

# Launch FastAPI app with auto-reload in dev mode
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
