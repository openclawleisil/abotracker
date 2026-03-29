from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///abos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Subscription(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    interval = db.Column(db.String(50), default='monthly')
    category = db.Column(db.String(100), default='General')
    notes = db.Column(db.Text, default='')

    def __repr__(self):
        return f"<Subscription {self.name} {self.amount}>"

# Ensure tables exist on startup (avoid relying on server hooks in some envs)
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    subs = Subscription.query.all()
    total = sum(s.amount for s in subs if s.interval=='monthly')
    return render_template('index.html', subs=subs, total=total)

@app.route('/add', methods=['POST'])
def add():
    name = request.form['name']
    amount = float(request.form['amount'])
    interval = request.form.get('interval','monthly')
    category = request.form.get('category','General')
    notes = request.form.get('notes','')
    s = Subscription(name=name, amount=amount, interval=interval, category=category, notes=notes)
    db.session.add(s)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    s = Subscription.query.get_or_404(id)
    db.session.delete(s)
    db.session.commit()
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
