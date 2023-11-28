from flask import Flask, render_template
import requests
from dotenv import load_dotenv, dotenv_values

config = dotenv_values('.env')
 
app=Flask(__name__)

def get_weather_data(city):
    API_KEY= config['API_KEY']
    url=f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&lang=es&units=metric'
    r = requests.get(url).json()
    print(r)
    return r

@app.route('/clima')
def clima():
    clima= get_weather_data('Cuenca')
    temperatura=str(clima['main']['temp'])
    descripcion=str(clima['weather'][0]['description'])
    icono=str(clima['weather'][0]['icon'])

    r_json={ 
        'ciudad':'Cuenca',
        'temperatura':temperatura,
        'descripcion':descripcion,
        'icono':icono}
    return render_template('weather.html',clima= r_json)

@app.route('/about1')
def about1():
    return render_template('CVanchundia.html')

@app.route('/about2')
def about2():
    return render_template('CVCHIRI.html')

@app.route('/about3')
def about3():
    return render_template('cvitalo.html')

@app.route('/about4')
def about4():
    return render_template('cvtomy.html')

@app.route('/about5')
def about5():
    return render_template('cvmacias.html')
    
@app.route('/about6')
def about6():
    return render_template('castañedacv.html')

if __name__ == '__main__':
    app.run(debug=True)