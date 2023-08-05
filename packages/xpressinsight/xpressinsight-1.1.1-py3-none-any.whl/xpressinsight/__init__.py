"""
    Xpress Insight Python package
    =============================

    The 'xpressinsight' Python package can be used to develop Python based web
    applications for Xpress Insight.

    (c) 2020 Fair Isaac Corporation
"""
#

__version__ = '1.1.1'  #

from .exec_mode import ExecMode, ExecModeRun, ExecModeLoad
from .types import (
    AppVersion, ResultData, ResultDataDelete, Manage, Hidden,
    boolean, integer, string, real,
    Scalar, Param, Index, Series, DataFrame, Column,
)
from .app_base import AppConfig, AppBase
from .interface import (
    Attachment,
    AttachmentRules,
    AttachStatus,
    AttachTag,
    AttachTagUsage,
    AppInterface,
    ObjSense,
    Metric,
)
from .interface_test import (
    read_attach_info,
    write_attach_info,
)
from .test_runner import create_app
