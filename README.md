[Description of the Dataset on the Coding daVinci Website](https://codingdavinci.de/daten/deutscher-reichsanzeiger-und-preussischer-staatsanzeiger)

# Ansights
Welcome to our Coding daVinci repository. Please don't judge us on the current state of the Code.
We  know it is very messy and not well documented, but we are working on that.
This Repository is the Backend of our project, providing a flask application that is called by out [ReactApp](https://github.com/SimeonAllmendinger/AppVisualAnzeights).
A Demo is currently hosted at [flyer-explorer.fiz-karlsruhe.de](https://flyer-explorer.fiz-karlsruhe.de)


![](data/animated_graph.gif)


### Partner Project
Also visit the Partner Project, which creates a Knowledge Graph with sparql-endpoint:
[flyer-explorer](https://github.com/ISE-FIZKarlsruhe/flyer-explorer)

## Run Development setup
### Setup the Repo
1. Clone this repo
2. 
    ```
    git submodule update --init --recursive
    ```
3. Create a venv/ conda env and enter it
4. 
    ```
    python3 -m pip install -r requirements.txt
    ```
5.
    ```
    python -m spacy download de_core_news_md
    ```
### Run the flask app
1. 
    ```
    cd src/flask_backend
    ```
2. 
    ```
    FLASK_DEBUG=0 python3 -m flask run
    ```

### Run the WebApp (in develop mode, not production)
1. 
    ```
    cd AppVisualAnzeights
    ```
2. 
    ```
    npm install
    ```
3. 
    ```
    npm run
    ```
    

# Dockerized Build
## Build an Run your the Docker Container
The latest docker image should be available to the right, under [packages](https://github.com/joelosw?tab=packages&repo_name=VisualAnzeights). Alternatively you can build it yourself:

Currently only a one-container setup is working:

1. 
```
docker build --tag anseights .
```
2. 
```
docker run --rm -p 80:3000 anseights
```