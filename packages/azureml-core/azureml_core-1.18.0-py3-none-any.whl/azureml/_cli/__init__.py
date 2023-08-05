# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

from azureml._base_sdk_common import __version__ as VERSION

from .aml_cli import AmlCli

__version__ = VERSION

AmlCli.add_subgroup_providers_from_entry_points()
