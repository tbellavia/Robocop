docker build -t discord-bot .
docker rm -f robocop
docker run -it --detach --name robocop discord-bot
