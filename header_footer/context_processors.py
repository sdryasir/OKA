from header_footer.models import Header, Footer

def navbar(request):
    header = Header.objects.all()
    footer = Footer.objects.all()
    return {"header": header, "footer": footer}