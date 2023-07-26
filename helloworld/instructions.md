# Instructions

Note: Generated with chatgpt + corrected issues

To run a simple "Hello World" Python application in a Kubernetes cluster with a single node, you'll need to follow several steps. But first, you'll need to have the following prerequisites installed on your system:

- Docker: for creating a container image of your Python application.
- Minikube: for running your single-node Kubernetes cluster.
- kubectl: for deploying and managing applications on your Kubernetes cluster.

Once the prerequisites are installed, you can proceed with the following steps:

## Step 1: Create Your Python Application

Create a new file named `app.py` and include the following Python code for a simple HTTP server:

```python
from http.server import BaseHTTPRequestHandler, HTTPServer

class HelloWorldHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "Hello, World!"
        self.wfile.write(bytes(message, "utf8"))
        return

def run():
  server_address = ('', 8000)
  httpd = HTTPServer(server_address, HelloWorldHandler)
  print('Running server...')
  httpd.serve_forever()

run()
```

This application starts a simple HTTP server that responds with "Hello, World!" to GET requests.

## Step 2: Create a Dockerfile

Next, create a Dockerfile in the same directory as your `app.py` file. This Dockerfile should define the steps to build an image of your application:

```Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . /app

CMD [ "python", "-u", "./app.py" ]
```

This Dockerfile does the following:

- Starts with a Python 3.9 base image.
- Sets `/app` as the working directory inside the container.
- Copies the current directory contents into the container at `/app`.
- Runs `app.py` when the container launches.

## Step 4: Start Your Kubernetes Cluster

Start your single-node Kubernetes cluster with the following command:

```bash
minikube start --driver=docker --container-runtime=containerd
```

## Step 3: Build the Docker Image

Next, build the Docker image with the following command:

```bash
docker build -t hello-world-python:latest .
```

This command builds the Docker image and tags it as `hello-world-python:latest`.

Uploads the image to minikube

```sh
minikube image load hello-world-python:latest
```

## Step 5: Create a Kubernetes Deployment

Next, create a Kubernetes Deployment to run your application. You can do this by creating a YAML file named `deployment.yaml` with the following content:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-world-python
spec:
  replicas: 1
  selector:
    matchLabels:
      app: hello-world-python
  template:
    metadata:
      labels:
        app: hello-world-python
    spec:
      containers:
      - name: hello-world-python
        image: hello-world-python:latest
        imagePullPolicy: Never
        ports:
        - containerPort: 8000
```

This Deployment creates one replica of your application and exposes it on port 8000.

```yaml
imagePullPolicy: Never
```

is specified because we use a local image accessible from minikube environment.

## Step 6: Apply the Kubernetes Deployment

Apply the Deployment with the following command:

```bash
minikube kubectl -- apply -f deployment.yaml
```

## Step 7: Create a Service to Expose Your Application

Finally, expose your application to the outside world by creating a Service. You can do this by creating a new YAML file named `service.yaml`:

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-world-python
spec:
  type: LoadBalancer
  ports:
    - port: 8000
  selector:
    app: hello-world-python
```

This Service exposes your application on a unique external IP address on your cluster.

Apply the Service with the following command:

```bash
minikube kubectl -- apply -f service.yaml
```

## Step 8: Access Your Application

Now, you can access your application by running the following command:

```bash
minikube service hello-world-python
```

This command opens your application in the default web browser.

That's it! You have successfully deployed a "Hello World" Python application to a single-node Kubernetes cluster.
