# Server States
STATES = {'STOPPED': 0, 'RUNNING': 1, 'RESTARTING': 2}

# Valid packet commands
COMMAND = [b'PING', b'PONG', b'HEART', b'BEAT', b'INFO', b'WARN', b'ERROR']