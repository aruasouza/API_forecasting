# Código principal

from src.server import server
from src.resources import *

app = server.app

if __name__ == '__main__':
    app.run(debug = True)