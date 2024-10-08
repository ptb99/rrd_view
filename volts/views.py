# volts/views.py - views for RRD viewer app

from django.shortcuts import get_object_or_404, render
from django.views.generic import TemplateView
from django.forms import modelformset_factory

from .models import graph,recipe_step,labels

# move this to another src-file?
import rrdtool

import subprocess
import logging


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'volts/index.html'

    def get_context_data(self, **kwargs):
        context = super(HomePageView, self).get_context_data(**kwargs)
        context['labels'] = labels.objects.first()
        context['graphs'] = graph.objects.all()
        return context


class AboutPageView(TemplateView):
    template_name = "volts/about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        context['labels'] = labels.objects.first()
        return context


class GraphView(TemplateView):
    template_name = "volts/graph.html"
    logger = logging.getLogger(__name__)

    def get_context_data(self, **kwargs):
        context = super(GraphView, self).get_context_data(**kwargs)
        context['labels'] = labels.objects.first()
        gr = get_object_or_404(graph, pk=kwargs['graph_id'])
        context['duration'] = gr.duration
        context['image'] = self.make_graph(gr)
        return context
    
    def make_graph(self, gr):
        graph_name = "volts-{0:s}.png".format(gr.duration)
        selector = gr.value_field
        ret = rrdtool.graph("./data/plot/{0:s}".format(graph_name),
                            "--start", "end-{0:s}".format(gr.duration),
                            "--end",  "now",
                            "--width", "1024", "--height", "300",
                            "--vertical-label={0:s}".format(gr.axis_label),
                            "--left-axis-format", "%.2lf",
                            "--rigid",
                            "--lower-limit", "{0:f}".format(gr.lower),
                            "--upper-limit", "{0:f}".format(gr.upper),
                            "--no-legend",
                            "DEF:volts=data/values.rrd:{0}:AVERAGE".format(selector),
                            "LINE3:volts#FF0000")
        self.logger.debug("rrdtool returns {}".format(ret))
        if ret:
            return graph_name
        else:
            return None


class RecipeView(TemplateView):
    """Handle form for setting up a Temp recipe"""
    template_name = 'volts/recipe.html'
    RecipeFormSet = modelformset_factory(recipe_step,
                                         fields=('target','duration'),
                                         extra=0)
    logger = logging.getLogger(__name__)

    def get(self, request, **kwargs):
        params = request.GET

        if 'start' in params:
            self.run_recipe()
            # set info message pane?

        if 'add' in params:
            val = params['add']
            self.add_steps(int(val))

        # both cases fall through to return the regular form (updated)
        formset = self.RecipeFormSet(queryset=recipe_step.objects.order_by('id'))
        l = labels.objects.first()
        return render(request, self.template_name,
                      {'formset': formset, 'labels': l})

    def post(self, request, **kwargs):
        # does this need a queryset too?
        formset = self.RecipeFormSet(request.POST)
        if formset.is_valid():
            formset.save()
        l = labels.objects.first()
        return render(request, self.template_name,
                      {'formset': formset, 'labels': l})

    def add_steps(self, value):
        """Increase or decrease number of steps in model"""
        if value > 0:
            while value > 0:
                recipe_step.objects.create()
                value = value - 1
        else:
            count = recipe_step.objects.count()
            if count + value < 1:
                # should prob throw exception here
                self.logger.warning ("BAD value for add: {}".format(value))
                return
            while value < 0:
                recipe_step.objects.last().delete()
                value = value + 1
        return

    def run_recipe(self):
        """Exec the current recipe"""
        args = ["./controller/controller.py"]
        for r in recipe_step.objects.order_by('id'):
            args.append(str(r.target))
            # convert hrs to secs
            dur = r.duration * 3600
            # flag 0 as meaning "forever" (i.e. stop processing args)
            if dur == 0.0:
                break
            else:
                args.append(str(dur))

        self.logger.debug('to exec: {}'.format(str(args)))
        # runs in the bg; could also use this to kill a prior instance??
        self.controller = subprocess.Popen(args)
