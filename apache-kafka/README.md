On PC startup run:

```bat
sudo docker rm $(sudo docker ps --filter status=exited -q)
sudo docker compose up -d
```