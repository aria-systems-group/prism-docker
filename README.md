# Dockerfile for running prism and prism-games
Only tested for Mac

# Prerequisite
- docker
- xquartz


# Build
```bash
docker build -t IMAGE_NAME .
```

e.g. `docker build -t prism .`

# Run
## Step 1
Open the setting in Xquartz and check the box that says "Allow connections from network clients". Then in terminal 1

```bash
xhost + 127.0.0.1
```

## Step 2
In terminal 2, run the following command to create a single use container

```bash
docker run -it --rm -p 22:22 -v $PWD/configs/prism/:/prism/configs/ -v $PWD/configs/prism-games/:/prism-games/configs/ IMAGE_NAME
```

e.g. `docker run -it --rm -p 22:22 -v $PWD/configs/prism/:/prism/configs/ -v $PWD/configs/prism-games/:/prism-games/configs/ prism`


To create a persistent container, run the following command (no `rm` tag)

```bash
docker run -it -p 22:22 -v $PWD/configs/prism/:/prism/configs/ -v $PWD/configs/prism-games/:/prism-games/configs/ --name CONTAINER_NAME IMAGE_NAME
```

## Step 3
In docker, to run `prism`,
```bash
cd /prism/prism/bin && ./prism
```

OR to run `prism GUI`

```bash
cd /prism/prism/bin && ./xprism
```

 To run `prism-games`

```bash
cd /prism-games/prism/bin && ./prism
```

OR to run `prism-games GUI`

```bash
cd /prism-games/prism/bin && ./xprism
```

## SSH Connection

The ssh server is running in the container by default. You can login by connecting to localhost(127.0.0.1) using the username `prism` and password `prism`. By default, the host's internal port `22` is mapped to container's ssh port `22`. You can change these ports while creating the container in `Step 2`.
