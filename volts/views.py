# volts/views.py - views for RRD viewer app

from django.shortcuts import render
from django.views.generic import TemplateView

from .models import graph

# move this to another src-file?
import rrdtool


# Create your views here.
class HomePageView(TemplateView):

    def get(self, request, **kwargs):
        choices = graph.objects.all()
        return render(request, 'volts/index.html', {'graphs': choices})


class AboutPageView(TemplateView):
    template_name = "volts/about.html"


class GraphView(TemplateView):
    # now just fixed params; should have a way to set or tune them
    upper = 12.5
    lower = 11.5

    def get(self, request, **kwargs):
        duration = kwargs['dur']
        img = self.make_graph(duration)
        context = {'duration': duration, 'image': img}
        return render(request, 'volts/graph.html', context)
    
    def make_graph(self, duration):
        graph_name = "volts-{0:s}.png".format(duration)
        #print("DBG: cwd = ", os.getcwd())
        ret = rrdtool.graph("./volts/static/{0:s}".format(graph_name),
                            "--start", "end-{0:s}".format(duration), 
                            "--end",  "now",
                            "--width", "800", "--height", "200",
                            "--vertical-label=Volts",
                            "--left-axis-format", "%.2lf",
                            "--rigid",
                            "--lower-limit", "{0:f}".format(self.lower), 
                            "--upper-limit", "{0:f}".format(self.upper),
                            "--no-legend",
                            "DEF:volts=voltage.rrd:voltage:AVERAGE",
                            "LINE3:volts#FF0000")
        #print("DBG: rrdtool returns ", ret)
        if ret:
            return graph_name
        else:
            return None
