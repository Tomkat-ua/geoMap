from flask import Flask
from gevent.pywsgi import WSGIServer
import folium,json,mgrs, urllib.request,os

location        = os.getenv("DEFUALT_LOCATION", [49.06830461667328, 33.41544936380822])
url             = os.getenv("JSON_URL", 'http://192.168.10.5:8082/get_map/json')
host_port       = os.getenv("HOST_PORT", 5000)
host_ip         = os.getenv("HOST_IP", '192.168.10.9')
app = Flask(__name__)



@app.route("/")
def fullscreen():
    response = urllib.request.urlopen(url)
    data0 = json.loads(response.read())
    first_key = list(data0)[0]
    mgrs_ = mgrs.MGRS()
    map = folium.Map(location=location, zoom_start=6)
    for row in data0[first_key]:
        marker = mgrs_.toLatLon(row['ACTION_COORD'])
        html = "<h4> " +row['TOV_NAME']+"</h4><br>"+ row['UNIT_PARENT_NAME']+"<br>"+str(row['ACTION_DATE'])+  "<br>"+ row['ACTION_PLACE']+"</p>"
        folium.Marker(location=marker, icon=folium.Icon(icon='info-sign', color='red'), popup=html).add_to(map)
    return map.get_root().render()

if __name__ == "__main__":
    # app.run(debug=True)
    http_server = WSGIServer((host_ip, host_port), app)
    http_server.serve_forever()
