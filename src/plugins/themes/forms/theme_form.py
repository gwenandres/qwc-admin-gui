import json

from flask_wtf import FlaskForm
from wtforms import FieldList, FormField, SelectField, BooleanField, \
        SelectMultipleField, IntegerField, StringField, SubmitField, \
        TextAreaField
from wtforms.validators import DataRequired, Optional, Regexp
from utils import i18n


class JSONField(TextAreaField):
    def _value(self):
        return json.dumps(self.data) if self.data else ''

    def process_formdata(self, valuelist):
        if valuelist:
            try:
                self.data = json.loads(valuelist[0])
            except ValueError:
                raise ValueError('This field contains invalid JSON')

class BackgroundLayerForm(FlaskForm):
    """Subform for backgroundlayers"""

    layerName = SelectField(coerce=str, validators=[DataRequired()])
    printLayer = StringField(validators=[Optional()])
    visibility = BooleanField(validators=[Optional()])

class QgisSearchForm(FlaskForm):
    """Subform for Qgis searches"""

    title = StringField(
        "Title",
        description="Search provider name.",
        validators=[DataRequired()]
    )
    featureCount = IntegerField(validators=[Optional()])
    resultTitle = StringField(validators=[Optional()])
    searchDescription = StringField(validators=[Optional()])
    defaultSearch = BooleanField(validators=[Optional()])
    group = StringField(validators=[Optional()])
    expression = JSONField(validators=[Optional()])
    fields = JSONField(validators=[Optional()])

class ThemeForm(FlaskForm):
    """Main form for Theme GUI"""

    url = SelectField(
        i18n('plugins.themes.theme.form_url'), 
        validators=[DataRequired()]
    )
    title = StringField(
        i18n('interface.common.title'),
        description=i18n('plugins.themes.theme.form_title_description'),
        validators=[Optional()]
    )
    attribution = StringField(
        i18n('plugins.themes.common.form_attribution'),
        description=(i18n('plugins.themes.theme.form_attribution_description')),
        validators=[Optional()]
    )
    thumbnail = SelectField(
        i18n('plugins.themes.common.form_thumbnail'),
        description=(i18n('plugins.themes.theme.form_thumbnail_description')),
        validators=[Optional()]
    )
    format = SelectField(
        i18n('plugins.themes.common.format'),
        description=(i18n('plugins.themes.theme.form_format_description')),
        validators=[Optional()]
    )
    mapCrs = SelectField(
        "CRS",
        description=i18n('plugins.themes.theme.form_crs_description'),
        default=("EPSG:3857"),
        validators=[Optional()]
    )
    additionalMouseCrs = SelectMultipleField(
        i18n('plugins.themes.theme.form_additionalMouseCrs'),
        description=(i18n('plugins.themes.theme.form_additionalMouseCrs_description')),
        validators=[Optional()]
    )
    searchProviders = SelectMultipleField(
        i18n('plugins.themes.theme.form_searchProviders'),
        description=i18n('plugins.themes.theme.form_searchProviders_description'),
        validators=[Optional()],
        default=("coordinates")
    )
    qgisSearchProvider = FieldList(FormField(QgisSearchForm))
    scales = StringField(
        i18n('plugins.themes.theme.form_scales'),
        description=i18n('plugins.themes.theme.form_scales_description'),
        default=(""),
        validators=[Optional(), Regexp(r'^(\d+)(,\s*\d+)*$',
                    message=i18n('plugins.themes.theme.form_scales_message'))]
    )
    printScales = StringField(
        i18n('plugins.themes.theme.form_printScales'),
        description=i18n('plugins.themes.theme.form_printScales_description'),
        default=(""),
        validators=[Optional(), Regexp(r'^(\d+)(,\s*\d+)*$',
                    message=i18n('plugins.themes.theme.form_printScales_message'))]
    )
    printResolutions = StringField(
        i18n('plugins.themes.theme.form_printResolutions'),
        description=i18n('plugins.themes.theme.form_printResolutions_description'),
        default=(""),
        validators=[Optional(), Regexp(r'^(\d+)(,\s*\d+)*$',
                    message=i18n('plugins.themes.theme.form_printResolutions_message'))]
    )
    printLabelBlacklist = StringField(
        i18n('plugins.themes.theme.form_printLabelBlacklist'),
        description=(i18n('plugins.themes.theme.form_printLabelBlacklist_description')),
        validators=[Optional(), Regexp(r'^(\w+)(,\s*\w+)*$',
                    message=i18n('plugins.themes.theme.form_printLabelBlacklist_message'))]
    )
    collapseLayerGroupsBelowLevel = IntegerField(
        i18n('plugins.themes.theme.form_collapseLayerGroupsBelowLevel'),
        description=i18n('plugins.themes.theme.form_collapseLayerGroupsBelowLevel_description'),
        validators=[Optional()]
    )
    default = BooleanField(
        i18n('plugins.themes.theme.form_default'),
        description=i18n('plugins.themes.theme.form_default_description'),
        validators=[Optional()]
    )
    tiled = BooleanField(
        i18n('plugins.themes.theme.form_tiled'),
        description=i18n('plugins.themes.theme.form_tiled_description'),
        validators=[Optional()]
    )
    mapTips = BooleanField(
        i18n('plugins.themes.theme.form_mapTips'),
        description=i18n('plugins.themes.theme.form_mapTips_description'),
        validators=[Optional()]
    )
    skipEmptyFeatureAttributes = BooleanField(
        i18n('plugins.themes.theme.form_skipEmptyFeatureAttributes'),
        description=i18n('plugins.themes.theme.form_skipEmptyFeatureAttributes_description'),
        validators=[Optional()]
    )

    backgroundLayers = FieldList(FormField(BackgroundLayerForm))

    submit = SubmitField(i18n('plugins.themes.common.form_submit'))
