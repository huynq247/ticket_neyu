import pandas as pd
import json
import csv
import logging
from typing import Dict, Any, Union, List, Optional
from io import BytesIO, StringIO
import base64
from datetime import datetime
import jinja2
import pdfkit
import os

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define supported export formats
SUPPORTED_FORMATS = ["json", "csv", "excel", "pdf", "html"]


def export_to_json(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Export data to JSON format
    """
    try:
        # Convert to JSON string
        json_str = json.dumps(data, indent=2, default=str)
        
        # Convert to base64 for easier transport
        json_bytes = json_str.encode('utf-8')
        base64_str = base64.b64encode(json_bytes).decode('utf-8')
        
        return {
            "content_type": "application/json",
            "filename": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "data": base64_str,
            "encoding": "base64"
        }
    except Exception as e:
        logger.error(f"Error exporting to JSON: {str(e)}")
        return {"error": str(e)}


def export_to_csv(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Export data to CSV format
    
    This function flattens the JSON structure to create a CSV file.
    Only summary data and basic metrics are included.
    """
    try:
        # Extract summary data or flatten complex structures
        if "summary" in data:
            summary = data["summary"]
        else:
            summary = data
        
        # Create a flat dictionary for CSV export
        flat_data = {}
        
        def flatten_dict(d, prefix=""):
            for key, value in d.items():
                if isinstance(value, dict):
                    flatten_dict(value, f"{prefix}{key}_")
                elif not isinstance(value, (list, dict)):
                    flat_data[f"{prefix}{key}"] = value
        
        flatten_dict(summary)
        
        # Add timestamp and metadata
        if "timestamp" in data:
            flat_data["timestamp"] = data["timestamp"]
        if "period_days" in data:
            flat_data["period_days"] = data["period_days"]
        
        # Convert to DataFrame for easy CSV export
        df = pd.DataFrame([flat_data])
        
        # Export to CSV
        csv_buffer = StringIO()
        df.to_csv(csv_buffer, index=False)
        
        # Convert to base64
        csv_bytes = csv_buffer.getvalue().encode('utf-8')
        base64_str = base64.b64encode(csv_bytes).decode('utf-8')
        
        return {
            "content_type": "text/csv",
            "filename": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            "data": base64_str,
            "encoding": "base64"
        }
    except Exception as e:
        logger.error(f"Error exporting to CSV: {str(e)}")
        return {"error": str(e)}


def export_to_excel(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Export data to Excel format
    
    This creates multiple sheets for different sections of the report
    """
    try:
        # Create an Excel writer
        excel_buffer = BytesIO()
        writer = pd.ExcelWriter(excel_buffer, engine='xlsxwriter')
        
        # Add summary sheet
        if "summary" in data:
            # Convert summary to DataFrame
            summary_data = []
            for key, value in data["summary"].items():
                if not isinstance(value, (dict, list)):
                    summary_data.append({"Metric": key, "Value": value})
                elif isinstance(value, dict):
                    # For dictionaries, create separate rows
                    for sub_key, sub_value in value.items():
                        summary_data.append({"Metric": f"{key}_{sub_key}", "Value": sub_value})
            
            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
        
        # Add metadata sheet
        metadata = {
            "Report Generated": data.get("timestamp", datetime.now().isoformat()),
            "Period (Days)": data.get("period_days", "N/A"),
        }
        metadata_df = pd.DataFrame([metadata])
        metadata_df.to_excel(writer, sheet_name='Metadata', index=False)
        
        # Save and close
        writer.close()
        
        # Get binary data
        excel_data = excel_buffer.getvalue()
        base64_str = base64.b64encode(excel_data).decode('utf-8')
        
        return {
            "content_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            "filename": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx",
            "data": base64_str,
            "encoding": "base64"
        }
    except Exception as e:
        logger.error(f"Error exporting to Excel: {str(e)}")
        return {"error": str(e)}


def export_to_html(data: Dict[str, Any], template_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Export data to HTML format using a template
    """
    try:
        # Use default template if none provided
        if not template_path:
            template_str = """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Report {{timestamp}}</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 20px; }
                    h1 { color: #333366; }
                    .summary { margin: 20px 0; padding: 10px; background-color: #f5f5f5; border-radius: 5px; }
                    .chart { margin: 20px 0; }
                    table { border-collapse: collapse; width: 100%; }
                    th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                    th { background-color: #f2f2f2; }
                </style>
            </head>
            <body>
                <h1>Report {{timestamp}}</h1>
                <p>Period: {{period_days}} days</p>
                
                <div class="summary">
                    <h2>Summary</h2>
                    <table>
                        <tr><th>Metric</th><th>Value</th></tr>
                        {% for key, value in summary.items() %}
                            {% if value is not mapping and value is not sequence %}
                            <tr><td>{{key}}</td><td>{{value}}</td></tr>
                            {% endif %}
                        {% endfor %}
                    </table>
                </div>
                
                {% if charts %}
                <div class="charts">
                    <h2>Charts</h2>
                    {% for chart_name, chart_data in charts.items() %}
                    <div class="chart">
                        <h3>{{chart_name}}</h3>
                        <img src="data:image/png;base64,{{chart_data}}" alt="{{chart_name}}">
                    </div>
                    {% endfor %}
                </div>
                {% endif %}
            </body>
            </html>
            """
            template = jinja2.Template(template_str)
        else:
            # Load template from file
            template_loader = jinja2.FileSystemLoader(searchpath=os.path.dirname(template_path))
            template_env = jinja2.Environment(loader=template_loader)
            template = template_env.get_template(os.path.basename(template_path))
        
        # Render HTML
        html_content = template.render(**data)
        
        # Convert to base64
        html_bytes = html_content.encode('utf-8')
        base64_str = base64.b64encode(html_bytes).decode('utf-8')
        
        return {
            "content_type": "text/html",
            "filename": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html",
            "data": base64_str,
            "encoding": "base64"
        }
    except Exception as e:
        logger.error(f"Error exporting to HTML: {str(e)}")
        return {"error": str(e)}


def export_to_pdf(data: Dict[str, Any], template_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Export data to PDF format
    
    First generates HTML, then converts to PDF
    """
    try:
        # Generate HTML first
        html_result = export_to_html(data, template_path)
        if "error" in html_result:
            return html_result
        
        # Decode HTML content
        html_content = base64.b64decode(html_result["data"]).decode('utf-8')
        
        # Convert HTML to PDF using pdfkit
        pdf_bytes = pdfkit.from_string(html_content, False)
        
        # Convert to base64
        base64_str = base64.b64encode(pdf_bytes).decode('utf-8')
        
        return {
            "content_type": "application/pdf",
            "filename": f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
            "data": base64_str,
            "encoding": "base64"
        }
    except Exception as e:
        logger.error(f"Error exporting to PDF: {str(e)}")
        return {"error": str(e)}


def export_report(data: Dict[str, Any], export_format: str, template_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Export report data to the specified format
    """
    if export_format not in SUPPORTED_FORMATS:
        return {
            "error": f"Unsupported format: {export_format}. Supported formats: {', '.join(SUPPORTED_FORMATS)}"
        }
    
    export_functions = {
        "json": export_to_json,
        "csv": export_to_csv,
        "excel": export_to_excel,
        "html": export_to_html,
        "pdf": export_to_pdf
    }
    
    if export_format in ["html", "pdf"] and template_path:
        return export_functions[export_format](data, template_path)
    else:
        return export_functions[export_format](data)