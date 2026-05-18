
from django.contrib import admin
from django.utils.html import format_html
from .models import LostItem, FoundItem

@admin.register(LostItem)
class LostItemAdmin(admin.ModelAdmin):
    # 1. 'name' is the link to the EDIT page. 
    # Adding 'edit_link' as a dedicated button column for clarity.
    list_display = ('display_image', 'name', 'status', 'category', 'location', 'date_reported', 'edit_button')
    
    # 2. Allows editing status and location without opening the item
    list_editable = ('status', 'location')
    
    # 3. Filtering and Searching
    list_filter = ('status', 'category', 'date_reported')
    search_fields = ('name', 'description', 'location')

    # 4. Custom Buttons
    def edit_button(self, obj):
        # Creates a blue 'Edit' button in the row
        return format_html('<a class="btn btn-info btn-sm" href="/admin/lostfounditerms/lostitem/{}/change/"><i class="fas fa-edit"></i> Edit</a>', obj.id)
    
    edit_button.short_description = 'Actions'

    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width: 40px; height:40px; border-radius: 4px;" />', obj.image.url)
        return "No Image"
    display_image.short_description = 'Img'

# Global Admin Customization for Jazzmin actions
admin.site.site_header = "LostFound Control Center"
admin.site.index_title = "System Management"