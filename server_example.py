import F4MP
server = F4MP.Server("127.0.0.1", 7779)


@server.listener()
def on_connection_request(event):
    pass

server.run()
