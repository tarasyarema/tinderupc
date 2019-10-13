sudo docker pull mongo
sudo docker run -d -p 27017:27017 --rm --name mongodb -v /home/ubuntu/tinderupc/db:/data/db mongo
