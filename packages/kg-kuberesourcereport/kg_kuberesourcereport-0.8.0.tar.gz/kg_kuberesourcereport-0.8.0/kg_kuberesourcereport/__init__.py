from .builder import (
    KubeResourceReportBuilder
)
from .option import (
    KubeResourceReportOptions,
    KubeResourceReportOptions_Default_Resources_Deployment,
    KubeResourceReportOptions_Default_Resources_DeploymentNGINX,
)

__version__ = "0.8.0"

__all__ = [
    'KubeResourceReportBuilder',
    'KubeResourceReportOptions',
    'KubeResourceReportOptions_Default_Resources_Deployment',
    'KubeResourceReportOptions_Default_Resources_DeploymentNGINX',
]
