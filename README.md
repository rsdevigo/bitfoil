# Bitfoil Fork

Set up a self-hosted Tinfoil shop to install backups of your games and updates from your computer onto your Switch over your network, and can download torrent files.

## Deployment

Modify the variables in the docker-compose.yaml file, then run it using Docker Compose.

```bash
docker compose -f ./docker-compose.yaml up -d --no-deps --build
```

![Docker Deploy](./assets/docker_deploy.png)

## Deployment on CasaOS

Do upload of docker-compose-casaos.yaml to CasaOS custom app install module. Configure all env variables and volumes. Then install the app on CasaOS.

## Downloading games

Get the torrent files and add on TORRENT_PATH on host machine of docker's containers.

## Screenshots

![Screenshot 1](./assets/screenshot_1.jpg)
![Screenshot 2](./assets/screenshot_2.jpg)
![Screenshot 3](./assets/screenshot_3.jpg)
![Screenshot 4](./assets/screenshot_4.jpg)
