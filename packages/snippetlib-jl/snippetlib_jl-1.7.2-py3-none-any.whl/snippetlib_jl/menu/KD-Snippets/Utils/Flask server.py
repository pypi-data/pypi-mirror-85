import flask

if __name__ == '__main__':

    app = flask.Flask(__name__)


    # NO ARGUMENT
    # Query with: curl http://localhost:8080
    @app.route("/")
    def index():
        return '<h1>Main</h1>'


    # ONE ARGUMENT
    # Query with: curl http://localhost:8080/station/Bonn%20Hbf
    @app.route("/station/<name>")
    def stationname(name):
        return 'Stationname: %s' %name


    # MULTIPLE ARGUMENTS
    # Query with: curl http://localhost:8080/coordinates/12.1/43.2
    @app.route("/coordinates/<lat>/<lon>")
    def coordinates(lat, lon):
        return '<b>Latitude:</b> %s<br />\n<b>Longitude:</b> %s' %(lat, lon)


    # JSON ARGUMENT VIA POST
    # Query with: curl -X POST http://localhost:8080/predict -d '{"datarecord": [1.0,2.7,3.1]}'
    @app.route('/predict', methods=['POST'])
    def predict():
        x = flask.request.get_json(force=True)['datarecord']
        response = {'rceived_datarecord': str(x)}
        return flask.jsonify(response)


    app.run(debug=False, host="127.0.0.1", port=8080, threaded=True)