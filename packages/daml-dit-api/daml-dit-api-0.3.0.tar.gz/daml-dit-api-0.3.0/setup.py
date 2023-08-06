# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['daml_dit_api']

package_data = \
{'': ['*']}

install_requires = \
['aiohttp', 'dazl>=7,<8']

setup_kwargs = {
    'name': 'daml-dit-api',
    'version': '0.3.0',
    'description': 'DABL DIT File API Package',
    'long_description': "daml-dit-api\n====\n\nAPI definitions for integrations and other sorts of packages to be\nhosted by DABL. This contains the following:\n\n* [The definition for the package metadata format](daml_dit_api/package_metadata.py)\n* [The call API for integration bots](daml_dit_api/integration_api.py)\n\n# Package Metadata\n\nAt their core, DIT files are [ZIP archives](https://en.wikipedia.org/wiki/Zip_(file_format))\nthat follow a specific set of conventions regarding their content. The\nmost important of these conventions is the presence of a YAML metadata\nfile at the root of the archive and named `dabl-meta.yaml`. This\nmetadata file contains catalog information describing the contents of\nthe DIT, as well as any packaging details needed to successfully\ndeploy a DIT file into DABL. An example of a deployment instruction is\na _subdeployment_. A subdeployment instructs DABL to deploy a specific\nsubfile within the DIT file. A DIT file that contains an embedded DAR\nfile could use a subdeployment to ensure that the embedded DAR file is\ndeployed to the ledger when the DIT is deployed. In this way, a DIT\nfile composed of multiple artifacts (DARs, Bots, UI's, etc.) can be\nconstructed to deploy a set of artifacts to a single ledger in a\nsingle action.\n\n# Integrations\n\nIntegrations are a special case of DIT file that are augmented with\nthe ability to run as an executable within a DABL cluster. This is\ndone by packaging Python [DAZL bot](https://github.com/DACH-NY/dazl)\ncode into an [executable ZIP](https://docs.python.org/3/library/zipapp.html)\nusing [PEX](https://github.com/pantsbuild/pex) and augmenting tha\nresulting file with the metadata and other resources needed to make it\na correctly formed DIT file.\n\nLogically speaking, DABL integrations are DAZL bots packaged with\ninformation needed to fit them into the DABL runtime and user\ninterface. The major functional contrast between a DABL integration\nand a Python Bot is that the integration has the external network\naccess needed to connect to an outside system and the Python Bot does\nnot. Due to the security implications of running within DABL with\nexternal network access, integrations can only be deployed with the\napproval of DA staff.\n\n## Developing Integrations\n\nThe easiest way to develop an integration for DABL is to use the\n[framework library](https://github.com/digital-asset/daml-dit-integration-framework)\nand [`ddit` build tool](https://github.com/digital-asset/daml-dit-ddit).\nThe integration framework presents a Python API closely related to the\nDAZL bot api and ensures that integrations follow the conventions\nrequired to integrate into DABL. The framework parses ledger\nconnection arguments, translates configuration metadata into a domain\nobject specific to the integration, and exposes the appropriate health\ncheck endpoints required to populate the DABL integration user\ninterface.\n\n_Unless you know exactly what you are doing and why you are doing it,\nuse the framework._\n\n### The Integration Runtime Environment\n\nBy convention, integrations accept a number of environment variables\nthat specify key paramaters.  Integrations built with the framework\nuse defaults for these variables that connect to a default locally\nconfigured sandbox instance.\n\nAvailable variables include the following:\n\n| Variable | Default | Purpose |\n|----------|---------|---------|\n| `DABL_HEALTH_PORT` | 8089 | Port for Health/Status HTTP endpoint |\n| `DABL_INTEGRATION_METADATA_PATH` | 'int_args.yaml' | Path to local metadata file |\n| `DABL_INTEGRATION_TYPE_ID` | | Type ID for the specific integration within the DIT to run |\n| `DABL_LEDGER_ID` | 'cloudbox' | Ledger ID for local ledger |\n| `DABL_LEDGER_URL` | `http://localhost:6865` | Address of local ledger gRPC API |\n",
    'author': 'Mike Schaeffer',
    'author_email': 'mike.schaeffer@digitalasset.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/digital-asset/daml-dit-api',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
