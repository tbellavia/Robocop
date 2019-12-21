docker build -t discord-bot .
docker rm -f robocop
docker run -it --detach --restart=always --name robocop discord-bot
