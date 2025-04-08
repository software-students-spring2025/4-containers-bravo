# Running the ML Client with Docker (Standalone)

Make sure you are inside the `machine-learning-client/` directory:

```bash
cd machine-learning-client
docker build -t sound-mood-client .
docker run sound-mood-client
