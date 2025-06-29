FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

# The internal port the container will listen on
EXPOSE 10000

# Use a shell to print a friendly startup message first, then start the server.
# It reads the PUBLIC_PORT from the .env file to create the correct clickable link.
CMD \
  echo "===================================================================" && \
  echo "🚀 MCQ from Topic application is running!" && \
  echo "✅ Open this link in your web browser:" && \
  echo "   http://localhost:${PUBLIC_PORT}" && \
  echo "===================================================================" && \
  waitress-serve --host=0.0.0.0 --port=10000 app:app