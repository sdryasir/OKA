from .models import Header, Footer

def navbar(request):
    header = Header.objects.all()
    
    # Fetch the first footer or adjust the query to fetch a specific one if needed
    footer = Footer.objects.first()
    
    # Prefetch related sections and links for efficiency
    sections = footer.sections.prefetch_related('links') if footer else []
    
    return {
        "header": header,
        "footer": footer,
        "sections": sections,
    }
