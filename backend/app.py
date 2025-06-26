from flask import Flask
from routes import register_routes
import os

app = Flask(
    __name__,
    template_folder=os.path.join('..', 'frontend', 'templates'),
    static_folder=os.path.join('..', 'frontend', 'static')
)
register_routes(app)

if __name__ == '__main__':
    app.run(debug=True) 