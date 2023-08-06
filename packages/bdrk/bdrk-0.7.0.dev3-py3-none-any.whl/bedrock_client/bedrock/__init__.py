import sys

from bdrk import model_analyzer  # noqa: F401 F403
from bdrk import monitoring  # noqa: F401 F403
from bdrk.tracking import client_old  # noqa: F401 F403

# Creating alias for backward compatible calls
sys.modules["bedrock_client.bedrock.api"] = client_old
sys.modules["bedrock_client.bedrock.metrics"] = monitoring
sys.modules["bedrock_client.bedrock.analyzer"] = model_analyzer
