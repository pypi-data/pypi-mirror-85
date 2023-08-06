from django.conf import settings

from haystack import indexes

# Not used here, but simplifies imports for apps
Indexable = indexes.Indexable  # noqa

if settings.HAYSTACK_SIGNAL_PROCESSOR == "celery_haystack.signals.CelerySignalProcessor":
    from celery_haystack.indexes import CelerySearchIndex as BaseSearchIndex
else:
    from haystack.indexes import SearchIndex as BaseSearchIndex


class SearchIndex(BaseSearchIndex):
    """Base class for search indexes on AlekSIS models.

    It provides a default document field caleld text and exects
    the related model in the model attribute.
    """

    text = indexes.EdgeNgramField(document=True, use_template=True)

    def get_model(self):
        return self.model
