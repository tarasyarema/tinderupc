sudo docker run -d -p 80:5000 --rm --name tinderupc -v ~/tinderupc:/app --env-file .env --network host tinderupc
