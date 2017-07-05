# -*- coding: utf-8 -*-
# © 2017 Elico Corp (https://www.elico-corp.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "Report Py3o Multisheet",
    "summary": """The new module 'report_py3o_multisheet' modifies the
    template required by 'report_py3o' module and adds multi-sheet
    management into the template""",
    "version": "10.0.1.0.0",
    "author": "Elico Corp",
    "support": "support@elico-corp.com",
    "license": "AGPL-3",
    "website": "https://www.elico-corp.com",
    "external_dependencies": {
        "python": ["ezodf"],
    },
    "depends": [
        "report_py3o",
    ],
    'data': [
        'security/ir.model.access.csv',
    ],
    "installable": True,
}
