import appoptics_apm.ao_logging
import appoptics_apm.inst_logging
from appoptics_apm.util import *
from appoptics_apm.version import __version__

# API for agent-internal logger
disable_logger = appoptics_apm.ao_logging.disable_logger
logger = appoptics_apm.ao_logging.logger

# API for agent configuration
config = AppOpticsApmConfig()

# Intialize agent
appoptics_apm_init()

# Report an status event after everything is done.
report_layer_init('Python')

appoptics_apm.inst_logging.wrap_logging_module()

# API for trace context in logs
get_log_trace_id = appoptics_apm.inst_logging.get_log_trace_id
