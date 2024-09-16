from mind_morphosis import app, db
from mind_morphosis.models import Users

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5500)