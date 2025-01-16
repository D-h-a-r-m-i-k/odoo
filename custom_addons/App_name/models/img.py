from email.policy import default
import requests
from odoo import fields,models,api,_
from datetime import date,datetime


from odoo.exceptions import ValidationError,UserError


class Img(models.Model):
    _name ='img.module' #model name (table name)
    _description = 'that tack a pic and create a new record' # that for the description of that module
    _rec_name = 'name' #that use for the record we created that show with that filed
    _order = 'age asc' #that is used for show the data in the order formate
    _inherit=['mail.thread','mail.activity.mixin'] #that is use for the show the chatter to for the tracking purposed

    #declere the fields (column name of that table)
    sequence=fields.Integer(string='seq.no',tracking=True)
    name=fields.Char(string='name',tracking=True)
    date_of_birth=fields.Date(string='DOB',tracking=True)
    age=fields.Integer(string='Age',help='Write a age',compute='_onchange_date_of_birth',store=True)
    cont_no=fields.Char(string='Cont.No',size=10,tracking=True)
    email=fields.Char(string='Email',tracking=True)
    hobie = fields.Many2many('user.tag', 'Img_tag_rel', 'lead_id', 'tag_id', string='Hobbies',help="Classify and analyze your lead/opportunity categories like: Training, Service",tracking=True)
    country_id = fields.Many2one(string="Country", comodel_name='res.country',help="Country for which this tag is available, when applied on taxes.",tracking=True,default=104)
    country_code=fields.Char(string='country code',related='country_id.code',tracking=True)
    state_id = fields.Many2one("res.country.state", string='State', readonly=False, store=True,domain="[('country_id', '=?', country_id)]",tracking=True)
    street = fields.Char('Street', readonly=False, store=True,tracking=True)
    street2 = fields.Char('Street2', readonly=False, store=True,tracking=True)
    post_office = fields.Selection(string="Post Office", selection=[], tracking=True)
    zip = fields.Char('Zip', change_default=True, readonly=False, store=True,tracking=True)
    city = fields.Char('City', readonly=False, store=True,tracking=True)
    details=fields.One2many('details.module','connecting_fields','details',tracking=True,copy=True, auto_join=True)
    status=fields.Selection([('active','Active'),('register','Register')],string='status',readonly=True,default='active',tracking=True)
    hand_salary=fields.Float('Hand salary',tracking=True)
    epf_esi=fields.Float('Epo+Esi',tracking=True)
    ctc_salary=fields.Float('CTC',compute='count_ctc',tracking=True)
    rating=fields.Selection([('0','low'),('1','medium'),('2','high'),('3','excellent')],'Rate me',tracking=True)
    currency_id = fields.Many2one('res.currency', 'Currency', related='country_id.currency_id', readonly=True,required=True)

    date=fields.Date('Current date',default=lambda self: date.today(),store=True)
    date_time=fields.Datetime(string='Current date & time',default= lambda self: datetime.now())
    User=fields.Many2one('res.users',string='User',default= lambda self: self.env.user.id)
    company=fields.Many2one('res.company',string='Company',default= lambda self:self.env.user.company_id.id)

    _sql_constraints = [('unique_name', 'UNIQUE(name)', 'The name must be unique')]
    # @api.model_create_multi
    # def write(self, vals):
    #     res=super(Img,self).write(vals)
    #     print(res)
    #     return res

    @api.onchange('zip')
    def _onchange_pin_code(self):
        if self.zip:
            try:
                # Call the API
                url = f"https://api.postalpincode.in/pincode/{self.zip}"
                response = requests.get(url)
                if response.status_code == 200:
                    data = response.json()
                    if data[0]['Status'] == 'Success':
                        # Populate Post Office names in the selection field
                        post_offices = data[0]['PostOffice']
                        self.post_office = False  # Reset selection
                        post_office_selection = [
                            (office['Name'], office['Name']) for office in post_offices
                        ]
                        self._fields['post_office'].selection = post_office_selection

                        # Default values from the first Post Office
                        default_office = post_offices[0]
                        self.city = default_office['District']
                        state_name = default_office['State']
                        country_name = default_office['Country']

                        # Fetch or create country and state
                        country = self.env['res.country'].search([('name', '=', country_name)], limit=1)
                        if country:
                            self.country_id = country.id
                        else:
                            self.country_id = self.env['res.country'].create({'name': country_name}).id

                        state = self.env['res.country.state'].search([('name', '=', state_name)], limit=1)
                        if state:
                            self.state_id = state.id
                        else:
                            self.state_id = self.env['res.country.state'].create({
                                'name': state_name,
                                'country_id': self.country_id.id
                            }).id

                        # Populate street2 with block, division, or additional details
                        self.street2 = f"{default_office['Block']}, {default_office['Division']}"

                    else:
                        self.city = self.state_id = self.country_id = self.street2 = self.post_office = False
                        return {'warning': {'title': "Invalid Pin Code", 'message': "No data found for this pin code."}}
                else:
                    return {'warning': {'title': "API Error", 'message': "Could not connect to the postal API."}}
            except Exception as e:
                return {'warning': {'title': "Error", 'message': str(e)}}

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id:
            self.country_id = self.state_id.country_id
        else:
            self.country_id = False

    @api.onchange('country_id')
    def _onchange_country_id(self):
        if not self.country_id:
            self.state_id = False

    def tata(self):
        data=self.env['res.config.settings'].search([])
        print(data)

    def unlink(self):
        for rec in self:
            if rec.status == 'register':
                raise UserError(_('record is register that way record is not delete'))
        return super(Img, self).unlink()

    @api.model
    def demo_report(self,vals):
        return  self.env.ref('App_name.action_report_demo_test_show').report_action(self.id)

    def meta_data(self):
        active_id = self.env.context.get('active_id')
        data=self.env['img.module'].browse(active_id)
        return {
            'name':data.name,
            'age':data.age,
        }

    # @api.model
    # def create(self, vals_list):
    #     res=super(Img,self).create(vals_list)
    #     if vals_list.get('name'):
    #         res['name']= res['name'].capitalize()
    #     print('self: ',self,' vals_list: ',vals_list,' rec: ',res)
    #     return res


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

    #that was mostly use for the show some validation Errors like show below
    # @api.constrains('age')
    # def val_age(self):
    #     for rec in self:
    #         if rec.age <=18:
    #             raise ValidationError(_('the age above then 18'))

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

    # #create orm method
    # def create_fun(self):
    #     print('create')

    #search orm method
    def search_fun(self):
        search_val=self.id
        print(search_val)


class Details(models.Model):
    _name = 'details.module'
    _description='that is use for the one to many filed and the data user will spend the mony'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    connecting_fields=fields.Many2one('img.module','connecting')
    sequence = fields.Integer(string='seq.no')
    product_id = fields.Many2one('product.product', string='product')
    quantity = fields.Float(string='Quantity')