# What
plain-paste means the data is plain, no encryption at all!

This is a part of my exercise to build pastebin using FastAPI and MongoDB.


# How
```
uvicorn app.main:app --reload
```

# deploy to fly.io
```
fly launch --no-deploy
fly deploy --ha=false
```