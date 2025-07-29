from flask import Flask
from models.model import db
from controllers.routes import init_routes
app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY']='4a778f29ce6868c886b0f979'

db.init_app(app)
init_routes(app)
with app.app_context():
    db.create_all()

if __name__=="__main__":
    app.run(debug=True)