# Criação do servidor que conterá os principais objetos

from flask import Flask
from flask_restful import Api
from src.security import Auth

class Server:
    def __init__(self):
        self.app = Flask(__name__)
        self.api = Api(self.app)
        self.auth = Auth


server = Server()