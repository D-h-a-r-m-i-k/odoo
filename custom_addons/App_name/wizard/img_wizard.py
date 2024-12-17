from odoo import fields,models,api,_
from datetime import date


from odoo.exceptions import ValidationError,UserError


class ImgWizard(models.TransientModel):
    _name ='img.module.wizard' #model name (table name)
    _description = 'that tack a pic and create a new record temporary base' # that for the description of that module
    _rec_name = 'name' #taht use for the record we created that show with that filed
    _order = 'age asc' #that is used for show the data in the order formate
    _inherit=['mail.thread','mail.activity.mixin'] #that is use for the show the chatter to for the tracking purposed

    #declere the fields (column name of that table)
    name=fields.Char(string='name')
    date_of_birth=fields.Date(string='DOB')
    age=fields.Integer(string='Age',help='Write a age',compute='_onchange_date_of_birth',store=True)
    cont_no=fields.Char(string='Cont.No',size=10)
    email=fields.Char(string='Email')
    country_id = fields.Many2one(string="Country", comodel_name='res.country',help="Country for which this tag is available, when applied on taxes.")
    country_code=fields.Char(string='country code',related='country_id.code')
    state_id = fields.Many2one("res.country.state", string='State',compute='_compute_partner_address_values', readonly=False, store=True,domain="[('country_id', '=?', country_id)]")
    street = fields.Char('Street', readonly=False, store=True)
    street2 = fields.Char('Street2', readonly=False, store=True)
    zip = fields.Char('Zip', change_default=True, readonly=False, store=True)
    city = fields.Char('City', readonly=False, store=True)
    details=fields.One2many('details.module.wizard','connecting_fields','details')

    hand_salary=fields.Float('Hand salary')
    epf_esi=fields.Float('Epo+Esi')
    ctc_salary=fields.Float('CTC',compute='count_ctc')
    rating=fields.Selection([('0','low'),('1','medium'),('2','high'),('3','excellent')],'Rate me')
    button_int=fields.Integer(string='Limit')

    


    @api.model
    def default_get(self, _fields):
        res = super(ImgWizard, self).default_get(_fields)
        active_id = self.env.context.get('active_id')
        lst=[]

        if active_id:
            main_model = self.env['img.module'].browse(active_id)
            for rec in main_model.details:
                lst.append((0,0,{'quantity':rec.quantity,'product_id':rec.product_id.id}))

            res.update({
                'name':main_model.name,
                'date_of_birth':main_model.date_of_birth,
                'age':main_model.age,
                'cont_no':main_model.cont_no,
                'email':main_model.email,
                'country_id':main_model.country_id.id,
                'country_code':main_model.country_code,
                'state_id':main_model.state_id.id,
                'street':main_model.street,
                'street2':main_model.street2,
                'zip':main_model.zip,
                'city':main_model.city,
                'hand_salary':main_model.hand_salary,
                'epf_esi':main_model.epf_esi,
                'ctc_salary':main_model.ctc_salary,
                'rating':main_model.rating,
                'details':lst,
                })
        return res


    #that is use for the calculation
    @api.depends('hand_salary','epf_esi')
    def count_ctc(self):
        for rec in self:
            ctc=0
            if rec.hand_salary:
                ctc+=rec.hand_salary
            if rec.epf_esi:
                ctc+=rec.epf_esi
            rec.ctc_salary=ctc


    @api.depends('date_of_birth')
    def _onchange_date_of_birth(self):
        for rec in self:
            if rec.date_of_birth:
                today = date.today()
                try:
                    rec.age = today.year - rec.date_of_birth.year - ((today.month, today.day) < (rec.date_of_birth.month, rec.date_of_birth.day))
                except Exception as e:
                    rec.age = 0
            else:
                rec.age = 0



    #that was used for the clear the one2many field
    def delete_fun_one2many(self):
        for rec in self:
            rec.details = [(5,0,0)]

    #that use for the show a effect like a rainbow man to success
    def state_register(self):
        for rec in self:
            rec.status='register'
        return {
            'effect':{
                'fadeout':'slow',
                'type':'rainbow_man',
                'message':'Data Register Successfully'
            }
        }

    #this is for that chang the state
    def state_active(self):
        for rec in self:
            rec.status='active'

    #object vise call the button
    def first_fun(self):
        print('hello world')


    #search orm method
    def search_fun(self):
        search_val=self.env.ref('App_name.view_img_module_form')
        print(search_val)


    def update_data(self):
        active_id = self.env.context.get('active_id')
        upd_var=self.env['img.module'].browse(active_id)

        if self.details:
            for rec in upd_var:
                rec.details = [(5, 0, 0)]

        lst1=[]
        for rec in self.details:
            lst1.append((0, 0, {'quantity': rec.quantity, 'product_id': rec.product_id.id}))

        vals={
            'name':self.name,
            'date_of_birth': self.date_of_birth,
            'age': self.age,
            'cont_no': self.cont_no,
            'email': self.email,
            'country_id': self.country_id.id,
            'country_code': self.country_code,
            'state_id': self.state_id.id,
            'street': self.street,
            'street2': self.street2,
            'zip': self.zip,
            'city': self.city,
            'hand_salary': self.hand_salary,
            'epf_esi': self.epf_esi,
            'ctc_salary': self.ctc_salary,
            'rating': self.rating,
            'details':lst1,
        }
        upd_var.write(vals)



class DetailsWizard(models.TransientModel):
    _name = 'details.module.wizard'
    _description='that is use for the one to many filed and the data user will spend the money'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    connecting_fields=fields.Many2one('img.module.wizard','connecting')
    sequence = fields.Integer(string='seq.no')
    product_id = fields.Many2one('product.product', string='product')
    quantity = fields.Float(string='Quantity')