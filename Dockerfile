FROM python:3.9

WORKDIR /app

# Copy only requirements.txt first to leverage Docker cache
COPY requirements.txt .

# Install dependencies in the virtual environment
RUN python -m venv venv && \
    . venv/bin/activate && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Use the virtual environment
ENV PATH="/app/venv/bin:$PATH"

CMD ["python", "run.py"]