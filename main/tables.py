import django_tables2 as tables
from django.contrib.auth.models import User

class UserTable(tables.Table):
    edit = tables.TemplateColumn(
        '<button type="button" onclick="openEditUserModal({{ record.id }}, \'{{ record.username }}\', \'{{ record.email }}\')">✏️ Edit</button>',
        orderable=False
    )
    delete = tables.TemplateColumn(
        '<a href="{% url "delete_user" record.id %}"><button>❌ Delete</button></a>',
        orderable=False
    )

    class Meta:
        model = User
        template_name = "django_tables2/bootstrap4.html"
        fields = ("id", "username", "email", "date_joined", "edit", "delete")
        orderable = False  # Disable sorting for all columns