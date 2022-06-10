FROM python:3.8-slim-buster
RUN git clone https://github.com/joelosw/VisualAnzeights app
RUN cd app && git submodule update --init --recursive
RUN RUN pip3 install -r requirements.txt
WORKDIR app/src/flask_backend
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]