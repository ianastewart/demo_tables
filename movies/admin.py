from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Movie


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    Admin interface for Movie model with comprehensive functionality.
    """
    
    # List display configuration
    list_display = [
        'title', 
        'release_date', 
        'movie_status', 
        'budget_display', 
        'revenue_display', 
        'profit_display',
        'vote_average', 
        'runtime_formatted',
        'created_at'
    ]
    
    list_filter = [
        'movie_status',
        'release_date',
        'created_at',
        'updated_at',
    ]
    
    search_fields = [
        'title',
        'overview',
        'tagline',
    ]
    
    list_editable = [
        'movie_status',
        'vote_average',
    ]
    
    readonly_fields = [
        'created_at',
        'updated_at',
        'profit_display',
        'profit_margin_display',
        'runtime_formatted',
        'is_released',
        'is_successful',
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'overview', 'tagline', 'homepage')
        }),
        ('Release Information', {
            'fields': ('release_date', 'movie_status', 'runtime', 'runtime_formatted')
        }),
        ('Financial Information', {
            'fields': ('budget', 'revenue', 'profit_display', 'profit_margin_display')
        }),
        ('Ratings & Popularity', {
            'fields': ('vote_average', 'vote_count', 'popularity')
        }),
        ('Status Properties', {
            'fields': ('is_released', 'is_successful'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    ordering = ['-release_date', 'title']
    date_hierarchy = 'release_date'
    list_per_page = 25
    
    def budget_display(self, obj):
        """Display budget with currency formatting."""
        if obj.budget:
            return f"${obj.budget:,}"
        return "-"
    budget_display.short_description = "Budget"
    budget_display.admin_order_field = "budget"
    
    def revenue_display(self, obj):
        """Display revenue with currency formatting."""
        if obj.revenue:
            return f"${obj.revenue:,}"
        return "-"
    revenue_display.short_description = "Revenue"
    revenue_display.admin_order_field = "revenue"
    
    def profit_display(self, obj):
        """Display profit with color coding."""
        profit = obj.profit
        if profit is None:
            return "-"
        
        color = "green" if profit > 0 else "red" if profit < 0 else "black"
        return format_html(
            '<span style="color: {};">${:,}</span>',
            color,
            profit
        )
    profit_display.short_description = "Profit"
    
    def profit_margin_display(self, obj):
        """Display profit margin as percentage."""
        margin = obj.profit_margin
        if margin is None:
            return "-"
        
        color = "green" if margin > 0 else "red" if margin < 0 else "black"
        return format_html(
            '<span style="color: {};">{:.1f}%</span>',
            color,
            margin
        )
    profit_margin_display.short_description = "Profit Margin"
    
    def get_queryset(self, request):
        """Optimize queryset for admin list view."""
        return super().get_queryset(request).select_related()
    
    def save_model(self, request, obj, form, change):
        """Custom save logic."""
        super().save_model(request, obj, form, change)
