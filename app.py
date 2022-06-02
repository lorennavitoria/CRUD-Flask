import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:{senha do banco de dados}@localhost/{nome do banco de dados criado}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)


class Celular(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    marca = db.Column(db.String(50))
    modelo = db.Column(db.String(100))
    sistemaOperacional = db.Column(db.String(5))
    memoriaRam = db.Column(db.String(6))
    pesoGrama = db.Column(db.Float(6))

    def __init__(self, marca, modelo, sistemaOperacional, memoriaRam, pesoGrama):
        self.marca = marca
        self.modelo = modelo
        self.sistemaOperacional = sistemaOperacional
        self.memoriaRam = memoriaRam
        self.pesoGrama = pesoGrama


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        celular = Celular(request.form['marca'], request.form['modelo'], request.form['sistemaOperacional'], request.form['memoriaRam'], request.form['pesoGrama'])
        db.session.add(celular)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    celular = Celular.query.get(id)
    if request.method == 'POST':
        celular.marca = request.form['marca']
        celular.modelo = request.form['modelo']
        celular.sistemaOperacional = request.form['sistemaOperacional']
        celular.memoriaRam = request.form['memoriaRam']
        celular.pesoGrama = request.form['pesoGrama']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit.html', celular=celular)



@app.route("/delete/<int:id>")
def delete(id):

    celular = Celular.query.get(id)#pega o estudante pelo ID
    db.session.delete(celular)#exclui o estudante
    db.session.commit()#salva
    return redirect(url_for('index'))#retorna o resultado para a página HTML 'index'



@app.route('/')
def index():
    celulares = Celular.query.all()
    return render_template('index.html', celulares=celulares)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
