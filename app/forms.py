from flask.ext.wtf import Form
from models import User
from wtforms import TextField, BooleanField, TextAreaField
from wtforms.validators import Required, Length


class LoginForm(Form):
  openid = TextField('openid', validators=[Required()])
  remember_me = BooleanField('remember_me', default=False)


class EditForm(Form):
  nickname = TextField('nickname', validators=[Required()])
  about_me = TextAreaField(
      'about_me', validators=[Length(min=0, max=140)])

  def __init__(self, original_name, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    self.original_name = original_name

  def validate(self):
    if not Form.validate(self):
      return False
    if self.nickname.data == self.original_name:
      return True
    user = User.query.filter_by(nickname=self.nickname.data).first()
    if user is not None:
      self.nickname.errors.append('This nickname is used, choose another one')
      return False
    return True
