# Use the official Python image from version 3.10 or upwards as the base image
FROM python:3.10

ARG GRADIO_SERVER_PORT=8082
ENV GRADIO_SERVER_PORT=${GRADIO_SERVER_PORT}

# Set working directory
WORKDIR /app

# Download the LLM model from the specified URL
RUN wget -O mistral-7b-openorca.Q4_0.gguf https://gpt4all.io/models/gguf/mistral-7b-openorca.Q4_0.gguf

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install required libraries from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python script to launch the Gradio app into the container
COPY main.py .

RUN chown -R 42420:42420 /app
ENV HOME=/app

# Set environment variables
ENV PORT=8082

# Expose the specified port
EXPOSE $PORT

# Command to launch the Gradio app on the specified port
CMD ["python", "main.py"]
