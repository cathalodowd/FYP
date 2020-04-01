from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from flask_wtf.file import FileField


class MapForm(FlaskForm):
    timetable = FileField()
    weekday = SelectField('What day do you want?:',
                          choices=[('Select', 'Select'), ('Sunday', 'Sunday'), ('Monday', 'Monday'),
                                   ('Tuesday', 'Tuesday'), ('Wednesday', 'Wednesday'), ('Thursday', 'Thursday'),
                                   ('Friday', 'Friday'), ('Saturday', 'Saturday')])
    submit = SubmitField('Submit')
