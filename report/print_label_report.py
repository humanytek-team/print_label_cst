# -*- coding: utf-8 -*-
###############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2017 Humanytek (<www.humanytek.com>).
#    Rubén Bravo <rubenred18@gmail.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

from openerp import api, models
import logging
_logger = logging.getLogger(__name__)


class PrintLabelProd2(models.AbstractModel):
    _name = 'report.print_label_cst.print_label_prod2'

    def decimal_format(self, num):
        return int(num)

    #def op_name(self, move_id):
        #StockMove = self.env['stock.move']
        #moves = StockMove.search([('move_dest_id.id', '=', move_id)])
        #if moves:
            #return moves[0].production_id.name
        #return ''

    def get_pick(self, product_id, line_id):
        StockMove = self.env['stock.move']
        moves = StockMove.search([('purchase_line_id.id', '=', line_id),
                                    ('product_id.id', '=', product_id),
                                    ('state', '!=', 'cancel')])
        if moves:
            if moves[0].picking_id:
                return moves[0].picking_id.name
        return ''

    @api.model
    def render_html(self, docids, data=None):
        Report = self.env['report']
        PurchaseOrder = self.env['purchase.order']
        report = Report._get_report_from_name(
            'print_label_cst.print_label_prod2')
        docs = PurchaseOrder.browse(docids)
        docargs = {
            'get_pick': self.get_pick,
            #'op_name': self.op_name,
            'decimal_format': self.decimal_format,
            'doc_ids': docids,
            'doc_model': report.model,
            'docs': docs,
            'data': data,
        }

        return Report.render('print_label_cst.print_label_prod2', docargs)

