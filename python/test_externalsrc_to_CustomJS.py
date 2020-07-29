from bokeh.io import show, output_file, save
from bokeh.plotting import figure
from bokeh.models import Div
from bokeh.models import ColumnDataSource

from bokeh.util.browser import view

from bokeh import events
from bokeh.models import  Label, LabelSet, CustomJS, TapTool, Toggle, Button, Spacer
import os

import numpy as np
import datetime
from datetime import date, timedelta

from bokeh.layouts import column, row, gridplot # For show multiple figures

# %% Assign output file
def filename(fullname):
    """ Return the name of a file without its path or extension"""
    return os.path.splitext(os.path.split(fullname)[1])[0]
output_filename = "../site/plots/"+os.path.basename(os.path.splitext(__file__)[0]) # name the output file/s after the script file
output_file(output_filename+".html",title=filename(output_filename))

# dummy plot, dunno why i need it
# p = figure()
# p.line([0,1],[0,1])

#%% Make State map buttons
tbutton = Toggle(label="County Time History Graph") #
tbutton.js_on_change('active',CustomJS(args={},code="""
        console.log('Hello Toggle button')
                  if (cb_obj.active == false){
                      cb_obj.label  = "Show Stuff"
                  }
                  else{
                      cb_obj.label  = "Hide Stuff"
                      }

// $.getJSON("../data/demo_data.json", function(data) { // This will not work on local files
$.getJSON("http://time.jsontest.com", function(data) { // This will not work on local files
var text = `Date: ${data.date}<br>
            Time: ${data.time}<br>
            Unix time: ${data.milliseconds_since_epoch}`
console.log(text)
});
                  """))
# Add
template = """
{% block postamble %}
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script>
    console.log('Hello template')
    </script>
{% endblock %}
"""

basic_template = """
{% from macros import embed %}

<!DOCTYPE html>
<html lang="en">
  {% block head %}
  <head>
    {% block inner_head %}
      <meta charset="utf-8">
      <title>{% block title %}{{ title | e if title else "Bokeh Plot" }}{% endblock %}</title>
      {% block preamble %}{% endblock %}
      {% block resources %}
        {% block css_resources %}
          {{ bokeh_css | indent(8) if bokeh_css }}
        {% endblock %}
        {% block js_resources %}
          {{ bokeh_js | indent(8) if bokeh_js }}
        {% endblock %}
      {% endblock %}
      {% block postamble %}{% endblock %}
    {% endblock %}
  </head>
  {% endblock %}
  {% block body %}
  <body>
    {% block inner_body %}
      {% block contents %}
        {% for doc in docs %}
          {{ embed(doc) if doc.elementid }}
          {% for root in doc.roots %}
            {% block root scoped %}
              {{ embed(root) | indent(10) }}
            {% endblock %}
          {% endfor %}
        {% endfor %}
      {% endblock %}
      {{ plot_script | indent(8) }}
    {% endblock %}
  </body>
  {% endblock %}
</html>
"""

external_src_template = """
{% from macros import embed %}

<!DOCTYPE html>
<html lang="en">
  {% block head %}
  <head>
    {% block inner_head %}
      <meta charset="utf-8">
      <title>{% block title %}{{ title | e if title else "Bokeh Plot" }}{% endblock %}</title>
      {% block preamble %}{% endblock %}
      {% block resources %}
        {% block css_resources %}
          {{ bokeh_css | indent(8) if bokeh_css }}
        {% endblock %}
        {% block js_resources %}
          {{ bokeh_js | indent(8) if bokeh_js }}
        {% endblock %}
      {% endblock %}
      {% block postamble %}

    <!-- Custom Added Code To Provide External Resources -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <script>
    console.log('Hello template')
    </script>

      {% endblock %}
    {% endblock %}
  </head>
  {% endblock %}
  {% block body %}
  <body>
    {% block inner_body %}
      {% block contents %}
        {% for doc in docs %}
          {{ embed(doc) if doc.elementid }}
          {% for root in doc.roots %}
            {% block root scoped %}
              {{ embed(root) | indent(10) }}
            {% endblock %}
          {% endfor %}
        {% endfor %}
      {% endblock %}
      {{ plot_script | indent(8) }}
    {% endblock %}
  </body>
  {% endblock %}
</html>
"""

# layout = row(p,tbutton)
layout = row(tbutton)
save(layout,template=external_src_template)
view(output_filename+'.html')
