from django.db.models import Q


def get_model_search(search_text: str, model_name: str) -> Q:
    search_map = {
        "post": Q(desc__icontains=search_text) | Q(title__icontains=search_text)
    }
    return search_map.get(model_name, Q())
