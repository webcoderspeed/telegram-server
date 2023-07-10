### Requirements
```
sudo apt-get update
sudo apt-get install python3

curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py

pip3 install fastapi[all]

pip3 install -r requirements.txt
```


### Start the server locally
```
uvicorn app.main:app --reload     
```

### Dockerise
```
  sudo service docker start

  docker build -t telegram-server .

  docker run -p 8000:8000 telegram-server


```


