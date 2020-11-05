FROM python:3
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chgrp -R 0 /app/api.py && \
    chmod -R g=u /app/api.py
USER 1001
EXPOSE 5000
CMD [ "python", "api.py" ]