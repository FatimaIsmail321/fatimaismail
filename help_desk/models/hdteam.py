# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class HdTeam(models.Model):
    _name = "hd.team"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name', required=True)

class Tags(models.Model):
    _name = "tags.tags"

    tage = fields.Char(string='Name')


class HdTicket(models.Model):
    _name = "hd.ticket"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # tecked = fields.Char(string='Name', required=True, copy=False, readonly=True,
    #                         default=lambda self: _('New'))
    tecked = fields.Char(string='Order tecked', required=True, copy=False, readonly=True,
                            default=lambda self: _('New'))
    name = fields.Char(string='Name', required=True)
    date_time = fields.Date(string="Timestamp")
    note = fields.Text(string='Description', required=True)
    team_id = fields.Many2one('hd.team', string="Team")
    assigned_id = fields.Many2one(
        'res.users', string='Assigned', tracking=True,
        default=lambda self: self.env.user)
    Priority = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], required=True, default='low', tracking=True)
    partner_id = fields.Many2one('res.partner', string="Customer",required=True)
    email = fields.Char("Email",related='partner_id.email', store=True)
    phone = fields.Char("Phone",related='partner_id.phone', store=True)
    tax_ids = fields.Many2many("tags.tags", string="Taxes")
    # tax_ids = fields.Many2many("account.tax", string="Taxes")

    hosting_type = fields.Selection([
        ('on-premise', 'On premise'),
        ('cloud', 'Cloud'),
    ], required=True, default='on-premise')
    resolution = fields.Date(string="Resolution")
    state = fields.Selection([('new', 'New'), ('in_Progress', 'In Progress'),
                              ('solved', 'Solved'), ('Cancelled', 'Cancelled')], default='new',
                             string="Status", tracking=True)
    ticket_count = fields.Integer(compute='compute_count')

    def compute_count(self):
        for record in self:
            record.ticket_count = self.env['fleet.vehicle'].search_count(
                [('driver_id', '=', self.id)])


    @api.model
    def create(self, vals):
        if vals.get('tecked', _('New')) == _('New'):
            vals['tecked'] = self.env['ir.sequence'].next_by_code('hd.ticket') or _('New')
        res = super(HdTicket, self).create(vals)
        return res

    def action_draft(self):
        self.state = 'Cancelled'


    def action_confirm(self):
        self.state = 'solved'

    def action_done(self):
        self.state = 'in_Progress'

    def action_cancel(self):
        self.state = 'cancel'

class ResPartner(models.Model):
    _inherit = 'res.partner'

    ticket_count = fields.Integer(compute='compute_count')

    def get_ticket(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Tickets',
            'view_mode': 'tree',
            'res_model': 'hd.ticket',
            'domain': [('assigned_id', '=', self.id)],
            'context': "{'create': False}"
        }
   
    def compute_count(self):
        for record in self:
            record.ticket_count = self.env['hd.ticket'].search_count(
                [('assigned_id', '=', self.id)])
    



   
   