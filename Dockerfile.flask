FROM python:3.9
RUN apt-get update
RUN apt-get install git -y
RUN apt-get install ffmpeg libsm6 libxext6  -y
# RUN git clone https://github.com/joelosw/VisualAnzeights /app
COPY . /app
WORKDIR /app
RUN cd /app && git submodule update --init --recursive
RUN pip3 install -r requirements.txt
RUN python -m spacy download de_core_news_md
WORKDIR /app/src/flask_backend
ENV FLASK_ENV production
ENV FLASK_DEBUG 0
EXPOSE 5000

CMD ["python3", "-m" , "flask", "run", "--host=0.0.0.0"]