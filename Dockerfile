# Use an official Python base image
FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the current project files to the container
COPY . .

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

RUN python -m nltk.downloader punkt stopwords
RUN python -m spacy download en_core_web_sm


# Expose the port Streamlit uses
EXPOSE 8501

# Run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
