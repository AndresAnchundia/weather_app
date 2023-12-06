from flask import Flask, render_template, request, url_for, redirect
import requests
from dotenv import load_dotenv, dotenv_values

from flask_sqlalchemy import SQLAlchemy 
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column

config = dotenv_values('.env')
app=Flask(__name__)


#creamos el contexto de la conexion
app.config["SQLALCHEMY_DATE_BASE_URI"]="sqlite.///weather.sqlite"

#Vinculamos la base de datos con la app
db= SQLAlchemy(app)

#Creamos el modelo
class City(db.Model):
    id: Mapped[int] = mapped_column(db.Integer, primary_key=True,autoincrement=True)
    name: Mapped[str] = mapped_column(db.String, unique=True, nullable=False)

#Con esta sentencia creamos la tabla
with app.app_context():
    db.create_all

def get_weather_data(city):
    API_KEY= config['API_KEY']
    url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=es&units=metric'
    r = requests.get(url).json()
    print(r)
    return r

@app.route('/clima', methods=['GET','POST'])
def clima():
    #Si es post es que pulson el boton Agregar Ciudad
    if request.method == 'POST':
        new_city=request.form.get('city')
        if new_city:
            obj = City(name=new_city)
            db.session.add(obj)
            db.session.commit()
            
    #llamo a todos las ciudades select * form city
    cities = City.query.all()
    weather_data =[]
    
    for city in cities:
        r=get_weather_data(city.name)
        weather = {
            'city' : city.name,
            'temperatura': r['main']['temp'],
            'descripcion': r['weather'][0]['description'],
            'icono': r['weather'][0]['icon'],
        }    
        weather_data.append(weather)
        
    return render_template('weather.html',weather_data=weather_data)    
    
@app.route('/delete_city/<name>')
def delete_city(name):
    city=City.query.filter_by(name=name).first()
    db.session.delete(city)
    db.session.commit()
    return redirect(url_for('clima'))    
    
    #clima= get_weather_data('Guayaquil')
    #temperatura=str(clima['main']['temp'])
    #descripcion=str(clima['weather'][0]['description'])
    #icono=str(clima['weather'][0]['icon'])

    #r_json={ 
    #    'ciudad':'Guayaquil',
    #    'temperatura':temperatura,
    #    'descripcion':descripcion,
    #    'icono':icono}
    #return render_template('weather.html',clima= r_json)

#ruta del curriculum
@app.route('/about')
def about1():
    return render_template('CVanchundia.html')

if __name__ == '__main__':
    app.run(debug=True)