FROM python:3.9-alpine
# FROM python:3.8.0
WORKDIR /app
RUN addgroup appuser && \
    adduser --system -u 1000 --no-create-home -G appuser appuser
RUN chown appuser:appuser /app
COPY --chown=appuser:appuser requirements.txt .
RUN pip install -r requirements.txt
COPY --chown=appuser:appuser . .
EXPOSE 8000
USER appuser
CMD [ "gunicorn", "-w", "3", "-b", "0.0.0.0:8000",\
 	  "--log-level", "debug", "app:app" ]
