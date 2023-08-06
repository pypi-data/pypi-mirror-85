import django_tables2 as tables

from utilities.tables import (
    BaseTable, BooleanColumn, ButtonsColumn, ColorColumn, ColoredLabelColumn,
    TagColumn, ToggleColumn,
)

from .models import Announcement


ANNOUNCEMENT_SUBJECT = """
{% if record.get_absolute_url %}
    <a href="{{ record.get_absolute_url }}">{{ record.subject }}</a>
{% else %}
    {{ record.subject }}
{% endif %}
"""

ANNOUNCEMENT_STATUS = """
<span class="label label-{{ record.status.status_label }}">{{ record.status }}</span>
"""

ANNOUNCEMENT_TYPE = """
<span class="label label-{{ record.get_type_class }}">{{ record.type }}</span>
"""

ANNOUNCEMENT_SERVER_TYPE = """
{% if record.server_type %}
    {{ record.server_type }}
{% else %}
    —
{% endif %}
"""

ANNOUNCEMENT_RELATED_SITE = """
<ul>
{% for site in record.related_site.all %}
    <li><a href="{{ site.get_absolute_url }}">{{ site }}</a></li>
    {% empty %}
        —
{% endfor %}
</ul>
"""

ANNOUNCEMENT_RELATED_DEVICE = """
<ul>
{% for device in record.related_device.all %}
    <li><a href="{{ device.get_absolute_url }}">{{ device }}</a></li>
    {% empty %}
        —
{% endfor %}
</ul>
"""

ANNOUNCEMENT_RELATED_VM = """
<ul>
{% for vm in record.related_vm.all %}
    <li><a href="{{ vm.get_absolute_url }}">{{ vm }}</a></li>
    {% empty %}
        —
{% endfor %}
</ul>
"""

ANNOUNCEMENT_CREATED_AT = """
<a href="{{ record.get_absolute_url }}">{{ value|date:"SHORT_DATETIME_FORMAT" }}</a>
"""

ANNOUNCEMENT_UPDATED_AT = """
<a href="{{ record.get_absolute_url }}">{{ value|date:"SHORT_DATETIME_FORMAT" }}</a>
"""

class AnnouncementButtonsColumn(tables.TemplateColumn):
    """
    Render edit and delete buttons for a announcement
    """
    buttons = ('edit', 'delete')
    attrs = {'td': {'class': 'text-right text-nowrap noprint'}}
    
    # Note that braces are escaped to allow for string formatting 
    # prior to template rendering
    
    template_code = """
    {{% if 'edit' in buttons and perms.{app_label}.change_{model_name} %}}
        {{% if record.type == 'network' %}}
            <a href="{{% url 'plugins:{app_label}:{model_name}_edit_network' {pk_field}=record.{pk_field} %}}?return_url={{{{ request.path }}}}" class="btn btn-xs btn-warning" title="Edit">
                <i class="fa fa-pencil"></i>
            </a>
        {{% elif record.type == 'server' and record.server_type == 'device' %}}
            <a href="{{% url 'plugins:{app_label}:{model_name}_edit_device' {pk_field}=record.{pk_field} %}}?return_url={{{{ request.path }}}}" class="btn btn-xs btn-warning" title="Edit">
                <i class="fa fa-pencil"></i>
            </a>
        {{% elif record.type == 'server' and record.server_type == 'vm' %}}
            <a href="{{% url 'plugins:{app_label}:{model_name}_edit_vm' {pk_field}=record.{pk_field} %}}?return_url={{{{ request.path }}}}" class="btn btn-xs btn-warning" title="Edit">
                <i class="fa fa-pencil"></i>
            </a>
        {{% else %}}
            <a href="{{% url 'plugins:{app_label}:{model_name}_edit' {pk_field}=record.{pk_field} %}}?return_url={{{{ request.path }}}}" class="btn btn-xs btn-warning" title="Edit">
                <i class="fa fa-pencil"></i>
            </a>
        {{% endif %}}
    {{% endif %}}
    {{% if 'delete' in buttons and perms.{app_label}.change_{model_name} %}}
        <a href="{{% url 'plugins:{app_label}:{model_name}_delete' {pk_field}=record.{pk_field} %}}?return_url={{{{ request.path }}}}" class="btn btn-xs btn-danger" title="Delete">
            <i class="fa fa-trash"></i>
        </a>
    {{% endif %}}
    """
    
    def __init__(self, model, *args, pk_field='pk', buttons=None, prepend_template=None, **kwargs):
        if prepend_template:
            prepend_template = prepend_template.replace('{', '{{')
            prepend_template = prepend_template.replace('}', '}}')
            self.template_code = prepend_template + self.template_code

        template_code = self.template_code.format(
            app_label=model._meta.app_label,
            model_name=model._meta.model_name,
            pk_field=pk_field,
            buttons=buttons
        )

        super().__init__(template_code=template_code, *args, **kwargs)

        self.extra_context.update({
            'buttons': buttons or self.buttons,
        })

    def header(self):
        return ''
    
    
class AnnouncementTable(BaseTable):
    """
    Announcement Table
    """
    subject = tables.TemplateColumn(
        template_code=ANNOUNCEMENT_SUBJECT,
        verbose_name='Subject'
    )
    slug = tables.Column(
        verbose_name='Slug'
    )
    user = tables.Column(
        verbose_name='Author'
    )
    status = tables.TemplateColumn(
        template_code=ANNOUNCEMENT_STATUS,
        verbose_name='Status'
    )
    content = tables.Column(
        verbose_name='Content'
    )
    type = tables.TemplateColumn(
        template_code=ANNOUNCEMENT_TYPE,
        verbose_name='Type'
    )
    server_type = tables.TemplateColumn(
        template_code=ANNOUNCEMENT_SERVER_TYPE,
        verbose_name='Server Type'
    )
    related_site = tables.TemplateColumn(
        template_code=ANNOUNCEMENT_RELATED_SITE,
        verbose_name='Related Site'
    )
    related_device = tables.TemplateColumn(
        template_code=ANNOUNCEMENT_RELATED_DEVICE,
        verbose_name='Related Device'
    )
    related_vm = tables.TemplateColumn(
        template_code=ANNOUNCEMENT_RELATED_VM,
        verbose_name='Related VM'
    )
    created_at = tables.TemplateColumn(
        template_code=ANNOUNCEMENT_CREATED_AT,
        verbose_name='Create Time'
    )
    updated_at = tables.TemplateColumn(
        template_code=ANNOUNCEMENT_UPDATED_AT,
        verbose_name='Last Update Time'
    )
    actions = AnnouncementButtonsColumn(
        model=Announcement, 
        buttons=('edit', 'delete'),
        pk_field='pk'
    )
    
    class Meta(BaseTable.Meta):
        model = Announcement
        fields = ('pk', 'subject', 'slug', 'user', 'content', 'status', 'type',
                  'server_type', 'related_site', 'related_device', 'related_vm', 
                  'created_at', 'updated_at', 'actions')
        default_columns = ('subject', 'status', 'user',
                           'updated_at', 'actions')
