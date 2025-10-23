import os # <-- 1. Importa 'os'
from flask import Flask, render_template, request, redirect
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from datetime import datetime

app = Flask(__name__)

# 2. Lee la MONGO_URI desde las variables de entorno
app.config["MONGO_URI"] = os.getenv("MONGO_URI") 

# 3. (Opcional) Verifica si la variable existe
if not app.config["MONGO_URI"]:
    raise ValueError("Error: No se encontró la variable de entorno MONGO_URI")

mongo = PyMongo(app)

# ... (El resto de tu código sigue exactamente igual)


@app.route('/update/<id>', methods=['GET', 'POST'])
def update(id):
    task = mongo.db.tasks.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        new_content = request.form['content']
        mongo.db.tasks.update_one({'_id': ObjectId(id)}, {'$set': {'content': new_content}})
        return redirect('/')
    return render_template('update.html', task=task)


@app.route('/delete/<id>')
def delete(id):
    mongo.db.tasks.delete_one({'_id': ObjectId(id)})
    return redirect('/')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        content = request.form['content']
        if content.strip():
            mongo.db.tasks.insert_one({'content': content, 'date_added': datetime.utcnow()})
        return redirect('/')
    
    tasks = mongo.db.tasks.find()
    return render_template('index.html', tasks=tasks, titulo="Task Master", mensaje="Con MongoDB")


if __name__ == "__main__":
    app.run(debug=True)