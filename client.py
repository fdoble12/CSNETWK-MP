def parse_input(input_string):
    command, *params = input_string.split()

    if command == '/join':
        # Connect to the server application
        # Syntax: /join <server_ip_add> <port>
        try:
            server_ip_add, port = params
        except:
            print("Error: Command parameters do not match or is not allowed.")

    elif command == 'leave':
        # Disconnect to the server application
        pass

    elif command == '/register':
        # Register a unique handle or alias
        # Syntax: /register <handle>
        try:
            [handle] = params
        except:
            print("Error: Command parameters do not match or is not allowed.")

    elif command == '/all':
        # Send message to all
        # Syntax: /all <message>
        message = ' '.join(params)

    elif command == '/msg':
        # Send direct message to a single handle
        # Syntax: /msg <handle> <message>
        try:
            handle = params[0]
            message = ' '.join(params[1:])
        except:
            print("Error: Command parameters do not match or is not allowed.")

    elif command == '/?':
        # Request command help to output all Input, Syntax commands for references
        pass

    else:
        print("Error: Command not found.")


if __name__ == "__main__":
    while True:
        user_input = input('>> ')
        parse_input(user_input)