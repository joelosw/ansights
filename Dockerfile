FROM python:3.8-slim-buster
RUN git clone https://github.com/joelosw/VisualAnzeights /app
RUN cd /app && git submodule update --init --recursive
RUN pip3 install -r requirements.txt
WORKDIR /app/src/flask_backend
CMD [ "FLASK_DEBUG=0", "python3", "-m" , "flask", "run", "--host=0.0.0.0"]