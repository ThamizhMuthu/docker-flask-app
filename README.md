# docker-flask-app

Small Flask app I containerized while learning Docker. Two endpoints, one Dockerfile, and a GitHub Actions workflow that builds it on every push.

## Endpoints

- `/` returns the container hostname, which is the container ID. Handy for seeing which instance answered when you run more than one.
- `/health` returns `{"status": "ok"}`. Load balancers and Kubernetes probes hit an endpoint like this to check the app is alive.

## Run it

```bash
docker build -t flask-app:v1 .
docker run -d -p 5001:5000 --name myapp flask-app:v1
curl http://localhost:5001
```

I map to 5001 on the host because macOS already uses port 5000 for AirPlay Receiver. Took me a while to work out why the container kept failing with "address already in use". The app itself still listens on 5000 inside the container.

## Things I learned building this

Flask has to bind to 0.0.0.0, not the default 127.0.0.1. Inside a container 127.0.0.1 only means the container itself, so the published port maps traffic in and Flask refuses it. Container looks healthy, connection gets reset.

requirements.txt gets copied before the app code on purpose. Docker caches each layer, so if the code went in first, every one-line edit would invalidate the pip install layer and reinstall Flask from scratch. Cheap steps last, expensive steps early.

Used python:3.12-slim rather than the full image. Roughly 150MB instead of about a gig, and fewer binaries sitting in there for someone to misuse if they ever get code execution.

Port comes from an environment variable with a fallback. Same image should run anywhere, only the environment changes.

## CI

`.github/workflows/ci.yml` builds the image on every push and curls /health to check it actually starts. Catches the case where the image builds fine but the app is broken.
