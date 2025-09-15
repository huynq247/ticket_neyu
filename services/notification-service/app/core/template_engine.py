from typing import Dict, Any, Optional
import jinja2

from app.models.template import get_template_by_name


class TemplateEngine:
    """Engine for rendering templates with Jinja2"""
    
    def __init__(self):
        # Create Jinja2 environment
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader("app/templates"),
            autoescape=jinja2.select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
        
        # Add custom filters
        self.env.filters['date'] = self._date_filter
        
    def _date_filter(self, value, format='%Y-%m-%d %H:%M:%S'):
        """
        Custom filter for formatting dates
        
        Args:
            value: Date value to format
            format: Date format string
            
        Returns:
            Formatted date string
        """
        if not value:
            return ""
        return value.strftime(format)
    
    def render_string(self, template_string: str, data: Dict[str, Any]) -> str:
        """
        Render a template string with provided data
        
        Args:
            template_string: Jinja2 template string
            data: Data to render template with
            
        Returns:
            Rendered template string
        """
        template = self.env.from_string(template_string)
        return template.render(**data)
    
    def render_template(self, template_name: str, data: Dict[str, Any]) -> Optional[str]:
        """
        Render a template from the database with provided data
        
        Args:
            template_name: Name of the template to render
            data: Data to render template with
            
        Returns:
            Rendered template string, or None if template not found
        """
        # Get template from database
        template_doc = get_template_by_name(template_name)
        if not template_doc:
            return None
            
        # Render template
        return self.render_string(template_doc["content"], data)


# Initialize template engine
template_engine = TemplateEngine()