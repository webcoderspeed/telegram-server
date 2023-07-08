### Requirements
- Install Python 3


### Start the server locally
```
uvicorn app.main:app --reload     
```

### Dockerise
```
  sudo service docker start

  docker build -t my-fastapi-server .

  docker run -p 8000:8000 my-fastapi-server


```


