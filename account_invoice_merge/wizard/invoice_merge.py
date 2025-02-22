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

from openerp.osv import osv, orm
from openerp.tools.translate import _


class invoice_merge(orm.TransientModel):
    _name = "invoice.merge"
    _description = "Merge Partner Invoice"

    def fields_view_get(self, cr, uid, view_id=None, view_type='form',
                        context=None, toolbar=False, submenu=False):
        """Changes the view dynamically

        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param context: A standard dictionary

        @return: New arch of view.

        """
        if context is None:
            context = {}
        res = super(invoice_merge, self).fields_view_get(
            cr, uid, view_id=view_id, view_type=view_type, context=context,
            toolbar=toolbar, submenu=False)

        if (
            context.get('active_model') == 'account.invoice'
            and len(context['active_ids']) < 2
        ):
            raise osv.except_osv(
                _('Warning'),
                _('Please select multiple invoice to merge in the list view.')
            )
        return res

    def merge_invoices(self, cr, uid, _ids, context=None):
        """To merge similar type of account invoices.

        @param self: The object pointer.
        @param cr: A database cursor
        @param uid: ID of the user currently logged in
        @param ids: the ID or list of IDs
        @param context: A standard dictionary

        @return: account invoice view

        """
        invoice_obj = self.pool.get('account.invoice')
        mod_obj = self.pool.get('ir.model.data')
        # None if sale is not installed
        so_obj = self.pool.get('sale.order')
        # None if purchase is not installed
        po_obj = self.pool.get('purchase.order')

        if context is None:
            context = {}
        try:
            search_view_id = mod_obj.get_object(
                cr, uid, 'account', 'view_account_invoice_filter'
            ).id
        except ValueError:
            search_view_id = False
        allinvoices = invoice_obj.do_merge(
            cr, uid, context.get('active_ids', []), context)

        for new_invoice in allinvoices:
            if so_obj is not None:
                todo_ids = so_obj.search(cr, uid, [
                    ('invoice_ids', 'in', allinvoices[new_invoice])
                ], context=context)
                for org_invoice in so_obj.browse(
                    cr, uid, todo_ids, context=context
                ):
                    so_obj.write(cr, uid, [org_invoice.id], {
                        'invoice_ids': [(4, new_invoice)]
                    }, context)
            if po_obj is not None:
                todo_ids = po_obj.search(cr, uid, [
                    ('invoice_ids', 'in', allinvoices[new_invoice])
                ], context=context)
                for org_invoice in po_obj.browse(
                    cr, uid, todo_ids, context=context
                ):
                    po_obj.write(cr, uid, [org_invoice.id], {
                        'invoice_ids': [(4, new_invoice)]
                    }, context)

        aw_obj = self.pool['ir.actions.act_window']
        ids = context.get('active_ids', [])
        invoices = invoice_obj.browse(cr, uid, ids, context=context)
        xid = {
            'out_invoice': 'action_invoice_tree1',
            'out_refund': 'action_invoice_tree3',
            'in_invoice': 'action_invoice_tree2',
            'in_refund': 'action_invoice_tree4',
        }[invoices[0].type]
        action = aw_obj.for_xml_id(cr, uid, 'account', xid, context=context)
        action.update({
            'domain': [('id', 'in', ids + allinvoices.keys())],
        })
        return action
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
