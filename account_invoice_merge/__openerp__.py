# -*- coding: utf-8 -*-
###############################################################################
#                                                                             #
#   Author: Leonardo Pistone <leonardo.pistone@camptocamp.com>                #
#   Copyright 2013 Camptocamp SA                                              #
#                                                                             #
#   Based on the merge Purchase Order functionality on OpenERP by OpenERP SA  #
#   the account_invoice_merge for 7.0 by Elico Corp, and work by              #
#   Romain Deheele, Camptocamp.                                               #
#                                                                             #
#   This program is free software: you can redistribute it and/or modify      #
#   it under the terms of the GNU Affero General Public License as            #
#   published by the Free Software Foundation, either version 3 of the        #
#   License, or (at your option) any later version.                           #
#                                                                             #
#   This program is distributed in the hope that it will be useful,           #
#   but WITHOUT ANY WARRANTY; without even the implied warranty of            #
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the             #
#   GNU Affero General Public License for more details.                       #
#                                                                             #
#   You should have received a copy of the GNU Affero General Public License  #
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.     #
#                                                                             #
###############################################################################

{
    'name': 'Account Invoice Merge Wizard',
    'version': '1.2',
    'category': 'Finance',
    'description': """
This module adds an action in the invoices lists to merge of invoices. Here are
the conditions to allow the merge:
- Type should be the same (customer Invoice, supplier invoice, Customer or
  Supplier Refund)
- Partner should be the same
- Currency should be the same
- Account receivable account should be the same
No merge is done at invoice line level.
    """,
    'author': "Camptocamp,Odoo Community Association (OCA)",
    'website': 'http://www.camptocamp.com',
    'depends': ['base', 'account'],
    'data': [
        'wizard/invoice_merge_view.xml',
    ],
    'test': [
    ],
    'demo': [],
    'installable': True,
    'active': False,
    'certificate': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
