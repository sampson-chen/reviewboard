from django.shortcuts import render_to_response
from django.template.context import RequestContext
def dashboard(request, template_name='xml_review_ui_extension/dashboard.html'):
    return render_to_response(template_name, RequestContext(request))
