from .models import Category

# When we add a context processor, we have to update our settings as well inside the templates>context processors with category.context_processors.category_links

# Now, we can call these in ANY template we want
def category_links(request):
    links = Category.objects.all()
    return dict(links=links)