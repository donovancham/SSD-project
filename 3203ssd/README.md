# Team 10 3203 

## Starting the app in docker
$ docker-compose up --build 
Visit http://localhost:5085

## Setting up for Windows
1.Clone the repo to anywhere </br>
2.Install and run the project, run:

1. py -3.9 -m venv venv
2. venv\Scripts\activate 
3. pip install -r requirements.txt
4. flask run --host=0.0.0.0 --port=5000

3.The application should be live on http://localhost:5000

## Notes
- Ensure virtual environment (venv) is enabled before staring the project with
```venv\Scripts\activate```
- Run ``` flask run --host=0.0.0.0 --port=5000 ``` to start the project
