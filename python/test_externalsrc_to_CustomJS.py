from bokeh.io import show, output_file, save
from bokeh.plotting import figure

from bokeh.util.browser import view

from bokeh.models import ColumnDataSource, CustomJS, Button, Toggle
from bokeh import events
from bokeh.layouts import column

import numpy as np

import os

import json
# Write the dummy data, casting the np.arrays because json doesn't support them
class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

# %% Make Dummy data
dummy_data = {
    'dummy_data_sin': {
        'x': np.arange(0,2*np.pi,0.1),
        'y': np.sin(np.arange(0,2*np.pi,0.1)),
        },
    'dummy_data_cos': {
        'x': np.arange(0,2*np.pi,0.1),
        'y': np.cos(np.arange(0,2*np.pi,0.1)),
        },
}

# thats human readable
path_data = '../site/data/'
rel_path_data = '../data/'
for dd in dummy_data:
    with open(path_data+dd+'.json', 'w') as outfile: json.dump(dummy_data[dd], outfile,cls=NumpyEncoder,indent=4, sort_keys=True)

# %% Assign output file
def filename(fullname):
    """ Return the name of a file without its path or extension"""
    return os.path.splitext(os.path.split(fullname)[1])[0]
output_filename = "../site/plots/"+os.path.basename(os.path.splitext(__file__)[0]) # name the output file/s after the script file
output_file(output_filename+".html",title=filename(output_filename))

# %% Make Dummy plot
p = figure()
source = ColumnDataSource(dummy_data['dummy_data_cos'])
l = p.line(x='x',y='y',source=source)

#%% Make State map buttons
tbutton = Toggle(label="County Time History Graph") #
tbutton.js_on_change('active',CustomJS(args={'rel_path_data':rel_path_data,'data_filenames':[k for k in dummy_data],'p':p, 'l':l},code="""

        console.log('Hello Toggle button')
            var N = data_filenames.length
                  if (cb_obj.active == false){
                      var ind_label = 1
                      var ind_data  = 0

                      var fullrel_path_data = rel_path_data+data_filenames[ind_data]+".json"
                      cb_obj.label  = "Show:"+data_filenames[ind_label]
                      console.log("Loading: "+fullrel_path_data)
                      $.getJSON(fullrel_path_data, function(data) { // This will not work on local files
                        l.data_source.data = data
                        l.data_source.change.emit()
                        console.log("Loaded:"+fullrel_path_data)
                      })
                  }
                  else{
                      var ind_label = 0
                      var ind_data = 1

                      var fullrel_path_data = rel_path_data+data_filenames[ind_data]+".json"
                      cb_obj.label  = "Show:"+data_filenames[ind_label]
                      console.log("Loading: "+fullrel_path_data)
                      $.getJSON(fullrel_path_data, function(data) { // This will not work on local files
                        l.data_source.data = data
                        l.data_source.change.emit()
                        console.log("Loaded:"+fullrel_path_data)
                      })
                  }
                  """))

# The following is the standard template that bokeh.io save and show use
# Sourced From: https://docs.bokeh.org/en/latest/docs/reference/core/templates.html
# Specifically from the section on FILE = <Template 'file.html'> ... Template:file.html

# basic_template = """
# {% from macros import embed %}
#
# <!DOCTYPE html>
# <html lang="en">
#   {% block head %}
#   <head>
#     {% block inner_head %}
#       <meta charset="utf-8">
#       <title>{% block title %}{{ title | e if title else "Bokeh Plot" }}{% endblock %}</title>
#       {% block preamble %}{% endblock %}
#       {% block resources %}
#         {% block css_resources %}
#           {{ bokeh_css | indent(8) if bokeh_css }}
#         {% endblock %}
#         {% block js_resources %}
#           {{ bokeh_js | indent(8) if bokeh_js }}
#         {% endblock %}
#       {% endblock %}
#       {% block postamble %}{% endblock %}
#     {% endblock %}
#   </head>
#   {% endblock %}
#   {% block body %}
#   <body>
#     {% block inner_body %}
#       {% block contents %}
#         {% for doc in docs %}
#           {{ embed(doc) if doc.elementid }}
#           {% for root in doc.roots %}
#             {% block root scoped %}
#               {{ embed(root) | indent(10) }}
#             {% endblock %}
#           {% endfor %}
#         {% endfor %}
#       {% endblock %}
#       {{ plot_script | indent(8) }}
#     {% endblock %}
#   </body>
#   {% endblock %}
# </html>
# """

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

    <!-- ############################################### -->
    <!-- Custom Added Code To Provide External Resources -->
    <script src="https://code.jquery.com/jquery-3.4.1.min.js"></script>
    <!-- ############################################### -->

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
layout = column(p,tbutton)
save(layout,template=external_src_template)
view(output_filename+'.html')
