### Requirements
- Install Python 3


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


