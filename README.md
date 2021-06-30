# Dockerfile for running prism and prism-games
Only tested for Mac

# Prerequisite
- docker
- xquartz


# Build
```bash
docker build -t IMAGE_NAME .
```

# Run
## Step 1
Open the setting in Xquartz and check the box that says "Allow connections from network clients". Then in terminal 1

```bash
xhost + 127.0.0.1
```

## Step 2
In terminal 2, run the following command

```bash
docker run -it --rm -v $PWD/configs/prism/:/prism/configs/ -v $PWD/configs/prism-games/:/prism-games/configs/ --name CONTAINER_NAME IMAGE_NAME bash
```

## Step 3
In docker, to run `prism`,
```bash
cd /prism/prism/bin && ./xprism
```

OR to run `prism-games`

```bash
cd /prism-games/prism/bin && ./xprism
```
