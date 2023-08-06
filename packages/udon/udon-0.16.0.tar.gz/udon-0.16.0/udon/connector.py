

class Connector:

    def __init__(self):
        pass

    def get_connection(self):
        with self.lock:
            if self.idle:
                cached = self.idle.pop()
                cached.connection_use()
                return conn

        conn = self.create_connection()
        cached = Connection(self, conn)
        self.connections.add(cached)
        return cached

    def create_connection(self):
        raise NotImplementedError


class Connection:

    def __init__(self, connector):
        self.connector = connector
