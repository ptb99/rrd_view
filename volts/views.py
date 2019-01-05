# volts/views.py - views for RRD viewer app

from django.shortcuts import get_object_or_404, render
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

    def get(self, request, **kwargs):
        gr = get_object_or_404(graph, pk=kwargs['graph_id'])
        img = self.make_graph(gr)
        context = {'duration': gr.duration, 'image': img}
        return render(request, 'volts/graph.html', context)
    
    def make_graph(self, gr):
        graph_name = "volts-{0:s}.png".format(gr.duration)
        selector = gr.value_field
        ret = rrdtool.graph("./volts/static/{0:s}".format(graph_name),
                            "--start", "end-{0:s}".format(gr.duration),
                            "--end",  "now",
                            "--width", "1024", "--height", "300",
                            "--vertical-label={0:s}".format(gr.axis_label),
                            "--left-axis-format", "%.2lf",
                            "--rigid",
                            "--lower-limit", "{0:f}".format(gr.lower),
                            "--upper-limit", "{0:f}".format(gr.upper),
                            "--no-legend",
                            "DEF:volts=temp.rrd:{0}:AVERAGE".format(selector),
                            "LINE3:volts#FF0000")
        #print("DBG: rrdtool returns ", ret)
        if ret:
            return graph_name
        else:
            return None
