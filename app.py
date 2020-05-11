import folium
import pandas as pd
from flask import Flask, render_template, url_for
from folium.plugins import MarkerCluster
import geocoder
from googleplaces import GooglePlaces, types, lang 
import requests 
import json 
import geopy.distance

app = Flask(__name__)

@app.route('/')

def index():
    dataset = pd.read_csv('lab_coordinate.csv')
    place = dataset[ ['Latitude', 'Longitude'] ]
    place=place.values.tolist()

    my_location = geocoder.ip('me')

    df_text = dataset['Test Lab Name']

    xlat = dataset['Latitude'].tolist()
    xlon = dataset['Longitude'].tolist()
    locations = list(zip(xlat, xlon))
    map2 = folium.Map(location=my_location.latlng, tiles='CartoDB dark_matter', zoom_start=8)
    marker_cluster = MarkerCluster().add_to(map2)

    title_html = '''
    			<style>
	                .button3 {border-radius: 8px;}

	                .button {
	                  background-color: #4CAF50; /* Green */
	                  border: none;
	                  color: white;
	                  padding: 15px 32px;
	                  text-align: center;
	                  margin-left: 42%;
			  margin-bottom: 10px;
	                  text-decoration: none;
	                  display: inline-block;
	                  font-size: 16px;
	                }
                </style>
             	 <h3 align="center" style="font-size:20px"><b>Covid-19 Active Test Lab In India</b></h3>
             	 '''

    map2.get_root().html.add_child(folium.Element(title_html))

    folium.Marker(
                location=my_location.latlng, 
                popup='Me',
                icon=folium.Icon(color='darkblue', icon_color='white', icon='male', angle=0, prefix='fa')
            ).add_to(map2)

    try:
        for point in range(0, len(locations)):
            folium.Marker(locations[point], 
                          popup = folium.Popup(df_text[point]),
                         ).add_to(marker_cluster)    
    except:
        pass
    # map2.save('map.html')

    return render_template('index.html')


@app.route("/detail/")
def detail():
    return render_template('detail.html')

@app.route("/nearMe/")
def nearMe():
    API_KEY = 'AIzaSyCJM2_o-SpAVPLrLXKL2-6JNeQRTbdUuno'
    google_places = GooglePlaces(API_KEY)
    
    my_location = geocoder.ip('me')
    lat, lng = my_location.latlng

    query_result = google_places.nearby_search( 
        lat_lng ={'lat': lat, 'lng': lng}, 
        radius = 5000, 
        types =[types.TYPE_HOSPITAL])

    name = []
    coord = []
    coords_1 = (lat, lng)
    # Iterate over the search results 
    for place in query_result.places:
        coords_2 = ( float(place.geo_location['lat']), float(place.geo_location['lng']))
        coord.append([ float(place.geo_location['lat']), float(place.geo_location['lng']) ])
        x = round(geopy.distance.distance(coords_1, coords_2).km, 5)
        if x >= 1:
            dis = " Distance: " + str(x) + "km"
        else:
            dis = " Distance: " + str(round(x*1000, 2)) + "m"
        
        name.append(place.name + dis)

    df_text = name
    
    locations = coord
    map2 = folium.Map(location=my_location.latlng, tiles='CartoDB dark_matter', zoom_start=12)

    marker_cluster = MarkerCluster().add_to(map2)

    title_html = '''
                 <h3 align="center" style="font-size:20px"><b>Hospitals And Medical Stores Near You</b></h3>
                 '''
    map2.get_root().html.add_child(folium.Element(title_html))

    folium.Marker(
                location=my_location.latlng, 
                popup='Your Location',
                icon=folium.Icon(color='darkblue', icon_color='white', icon='male', angle=0, prefix='fa')
            ).add_to(map2)

    folium.Circle(
        location=[lat, lng],
        radius=5000,
        color='#3186cc',
        fill=True,
        fill_color='#3186cc'
    ).add_to(map2)

    for point in range(0, len(locations)):
            folium.Marker(locations[point], 
                          popup = folium.Popup(df_text[point]),
	                     ).add_to(marker_cluster)
    map2.save('templates/nearMe.html')
    
    return render_template('nearMe2.html')


if __name__ == '__main__':
    app.run(debug=True)
