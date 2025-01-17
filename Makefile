clean:
	echo '' > redis.logs
	
watchlogs:
	tail -f redis.logs

server: clean
	@python3 main.py -t server

client:
	@python3 main.py -t client
