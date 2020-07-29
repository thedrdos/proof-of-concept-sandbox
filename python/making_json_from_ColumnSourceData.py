import numpy as np
import json

# Problem is that ns arrays arent supported so if
source = ColumnSourceData(org_data)
data = source.data
# then normally data can't be dumped to a json

# However, the following seems to work

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

# to a string variable
dumped = json.dumps(data, cls=NumpyEncoder)

# Or to a file
with open('data.json', 'w') as outfile: json.dump(data, outfile,cls=NumpyEncoder)

# thats human readable
with open('data.json', 'w') as outfile: json.dump(data, outfile,cls=NumpyEncoder,indent=4, sort_keys=True)
