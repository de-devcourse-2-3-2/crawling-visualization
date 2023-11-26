FROM python:3.11
WORKDIR /crawling_visualization
COPY ./crawling /crawling_visualization/crawling
COPY ./musinsa_trend /crawling_visualization/musinsa_trend
COPY ./requirements.txt /crawling_visualization
COPY ./logger.py /crawling_visualization
RUN apt-get update
RUN python -m venv venv
RUN . venv/bin/activate
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
WORKDIR /crawling_visualization/musinsa_trend
#CMD ["python3", "manage.py", "runserver", "localhost:8000"]
CMD ["python3", "manage.py", "migrate"]
#EXPOSE 8000