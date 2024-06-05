GET STARTED-
  Oh just open the top directory for the repo and run the command 'sudo docker build -t maxsessionssite ." And itll build the docker image. Alternatively you can run

  "python3 -m venv devenv"
  ". ./devenv/bin/activate"
  "pip install --upgrade pip"
  "pip install -r requirements.txt"
  "gunicorn wsgi:app"

  And itll boot right up for testing and development. Once youve done the dev set up once you just go to the top directory where the /devenv directory is and run

  ". ./devenv/bin/activate"
  "gunicorn wsgi:app"

  To get up and going again
