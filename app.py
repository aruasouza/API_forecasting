from website.app import app
import os

if __name__ == '__main__':
    os.environ['AUTHLIB_INSECURE_TRANSPORT'] = "1"
    app.run(debug = False,port = 5000)