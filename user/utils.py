from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa

def render_to_pdf(template_src,context_dict={}):
    template = get_template(template_src)
    # template = open('../templates/online/get_group_pupils.html', 'rb')
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('utf-8')), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


#
# if download:
#             template_name = 'online/get_group_pupils.html'
#             pdf = render_to_pdf(template_name, context)
#             if pdf:
#                 response = HttpResponse(pdf, content_type='application/pdf')
#                 filename = f"{group.category}-{group.number} {group.year}.pdf"
#                 #pdfni yuklab olish attachment
#                 content = "attachment; filename=%s" % (filename)
#                 response['Content-Disposition'] = content
#                 return response