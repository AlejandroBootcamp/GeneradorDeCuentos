# Use the official Python image
FROM python:3.13.2

# Set the working directory
WORKDIR /app

# Copy all files to the container
COPY backend/ /app/backend
COPY frontend/ /app/frontend
COPY __main__.py /app/
COPY requirements.txt /app/
COPY entrypoint.sh /app/
COPY apis.txt /app/.env

# Install dependencies :: (RUN es solo cuando se genera el container)
RUN pip install -r requirements.txt

# Expose Streamlit's default port
EXPOSE 8501

# Run the app
CMD ["/app/entrypoint.sh"]