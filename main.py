# from idlelib.replace import replace

from flask import Flask#, render_template_string
from gevent.pywsgi import WSGIServer
import folium,json,fbextract,mgrs
import urllib.request

app = Flask(__name__)
location=[49.06830461667328, 33.41544936380822]

with open("qrys.json", "r") as f:
    q = json.load(f)
#
# text = json.loads('http://192.168.10.5:8082/get_map/json')

url = "http://192.168.10.5:8082/get_map/json"
# def get_mapdata(url):
#     response = urllib.request.urlopen(url)
#     data0 = json.loads(response.read())
#     first_key = list(data0)[0]
#     mgrs_ = mgrs.MGRS()
#     for row in data0[first_key]:
#         # marker = row['ACTION_COORD']
#         marker = mgrs_.toLatLon(row['ACTION_COORD'])
#         print(marker)
#
#
# get_mapdata(url)



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

    # map = folium.Map(location=location, zoom_start = 6)
    # data = fbextract.get_data(q['GET_MAP'])
    # for row in data:
    #     print(row)
    #     m = mgrs.MGRS()
    #     locmarker = m.toLatLon(row[1])
    #     html = """<h4> """ +row[0]+"""</h4><br>"""+ row[4]+"""<br>"""+str(row[3])+"""<br>"""+ row[2]+"""</p>"""
    #     folium.Marker(location=locmarker, icon=folium.Icon(icon='info-sign', color='red'), popup=html).add_to(map)
    return map.get_root().render()

# map.save("map1.html")


if __name__ == "__main__":
    # app.run(debug=True)
    http_server = WSGIServer(('192.168.10.9', 5001), app)
    http_server.serve_forever()
