from import_export import resources
from .models import SIShipped


class ExcelResources(resources.ModelResource):
    class Meta:
        model = SIShipped