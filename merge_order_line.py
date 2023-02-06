from odoo import models, api


class MergerOrderLine(models.Model):
    _inherit = 'sale.order'

    @api.model
    def action_confirm(self):
        for line in self.order_line:
            if line.id in self.order_line.ids:
                line_ids = self.order_line.filtered(
                    lambda m: m.product_id.id == line.product_id.id and m.
                    price_unit == line.price_unit)
                quantity = 0
                for qty in line_ids:
                    quantity += qty.product_uom_qty
                    line_ids.write({'product_uom_qty': quantity,
                                    'order_id': line_ids.order_id.id,
                                    'price_unit': line.price_unit})
                line_ids[1:].unlink()
        res = super(MergerOrderLine, self).action_confirm()
        return res
