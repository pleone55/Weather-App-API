from django.shortcuts import render, redirect
import requests
from .models import City
from .forms import CityForm

def index(request):
    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=9c232263729a5d8323c4c23d763742c7'
    
    errorMsg = ''
    message = ''                #message the user will see
    message_class = ''          #the color the message will be
    
    if request.method == 'POST':
        form = CityForm(request.POST)
        
        if form.is_valid():
            new_city = form.cleaned_data['name']
            #filter out cities that have already been added
            exisiting_city = City.objects.filter(name=new_city).count()
            
            if exisiting_city == 0:
                r = requests.get(url.format(new_city)).json()
                #find city code to determine if city exists
                #print(r)
                if r['cod'] == 200:
                    form.save()
                else:
                    errorMsg = 'City does not exist!'
            else:
                errorMsg = "City already exists!"
        if errorMsg:
            message = errorMsg
        else:
            message = 'City added successfully!'
    
    #restart the form after submission
    form = CityForm()
    
    cities = City.objects.all()
    
    weather_data = []
    
    #loop thru each city in the database
    for city in cities:
        #call the requests to add the city to the url
        #call the json method to convert information to a json object
        r = requests.get(url.format(city)).json()
        
        #print was used to gather the neccessary information on the command line
        #print(r.text)
        
        #create a dictionary that holds the information needed to display the weather
        city_weather = {
            'city': city.name,                  #pass the name of the object not the object itself
            'temperature': r['main']['temp'],
            'description': r['weather'][0]['description'],
            'icon': r['weather'][0]['icon'],
        }
        
        #append the weather data to each city
        weather_data.append(city_weather)
    
    print(weather_data)
    
    context = {'weather_data': weather_data,
                'form': form,
                'message': message,
                }
    return render(request, 'weather/weather.html', context)

def delete_city(request, city_name):
    #query the city and delete it
    City.objects.get(name=city_name).delete()
    return redirect('home')
