import collectd
import subprocess
import xml

# nvidia-smi command
NV_CMD = ["nvidia-smi", "-q", "-x"]

import sys
if sys.version_info[0] < 3:
    # python 2
    def _subproc_call():
        return subprocess.check_output(NV_CMD) 
else:
    # python 3
    def _subproc_call():
        data = subprocess.run(NV_CMD, stdout=subprocess.PIPE)
        return data.stdout

gpu_queries = {
    "fb_memory_usage": ["used", "free", "total"],
    "utilization": ["gpu_util", "memory_util", "encoder_util", "decoder_util"],
    "temperature": ["gpu_temp"],
    "power_readings": ["power_draw", "power_limit", "enforced_power_limit", "max_power_limit"],
    "general": ["fan_speed"]
}

def init(*args, **kwargs):
    """ plugin init """
    collectd.info("init gpu_monitor")

def read(*args, **kwargs):
    """ read callback """
    global gpu_queries
    vl = collectd.Values(type='gauge')
    vl.plugin = "python.gpu_monitor"
    
    data = _subproc_call()
    root = xml.etree.ElementTree.fromstring(data)

    for gpu in root.getiterator('gpu'):

        vl.plugin_instance = 'cuda-{}'.format(gpu.attrib['id'])

        for _type, nest in gpu_queries.items():

            for instance in nest:
                if _type == "general":
                    # root level
                    query = instance
                else:
                    # sublevel
                    query = "{}/{}".format(_type, instance)

                try:
                    value = float(gpu.find(query).text.split(" ")[0])
                except:
                    collectd.warning("Could not find query {}".format(query))
                else:
                    vl.dispatch(type_instance=query, values=[value])

# register callbacks
collectd.register_init(init)
collectd.register_read(read)
