import cherrypy
import os

class Execute(object):
    @cherrypy.expose
    def index(self):
        with open('index.html', 'r') as file:
            data = file.read().replace('\n', ' ')
        return data

    @cherrypy.expose
    def solid_color(self, r=None, g=None, b=None, bright=None):
        os.popen(f"sudo python3 controller.py -s {r},{g},{b} -b {bright}")
        with open('index.html', 'r') as file:
            data = file.read().replace('\n', ' ')
        return data

    @cherrypy.expose
    def pattern_color(self, p=None):
        if p:
            os.popen(f"sudo python3 controller.py -q {p}")
        with open('index.html', 'r') as file:
            data = file.read().replace('\n', ' ')
        return data

con = os.path.join(os.path.dirname(__file__), 'config.conf')

if __name__ == '__main__':
    cherrypy.quickstart(Execute(), config=con)
#    app.run(debug=True, port=80, host='0.0.0.0', threaded=True)
