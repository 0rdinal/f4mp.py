import F4MP

server = F4MP.Server("localhost", 7779)


@server.listener()
def on_connection_request(event):
    print('connection requested')

@server.listener()
def on_connection_accepted(event):
    print('connection accepted')


server.run()
