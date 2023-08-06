""" HTML Enhancer : get instances of HTML enhancements. """

from .article_schema_creator import ArticleSchemaCreator
from .breadcrumb_schema_creator import BreadcrumbSchemaCreator
from .canonical_url_creator import CanonicalURLCreator


class HTMLEnhancer:
    """ HTML Enhancer : get instances of HTML enhancements. """

    def __init__(self, file, output_path, path):
        _settings = getattr(file, "settings")
        _author = getattr(file, "author", None)
        _date = getattr(file, "date", None)
        _title = getattr(file, "title", None)
        _category = getattr(file, "category", None)
        _image = getattr(file, "image", None)
        _metadata = getattr(file, "metadata", None)

        self.article_schema = ArticleSchemaCreator(
            author=_author,
            title=_title,
            category=_category,
            date=_date,
            logo=_settings.get("LOGO"),
            image=_image,
            sitename=_settings.get("SITENAME"),
        )

        # The canonical URL must be built with custom metadata if filled
        # If not, fallback to the default URL name
        save_as = _metadata.get("save_as")
        _fileurl = save_as if save_as else getattr(file, "url")

        self.canonical_link = CanonicalURLCreator(
            siteurl=_settings.get("SITEURL"), fileurl=_fileurl,
        )

        self.breadcrumb_schema = BreadcrumbSchemaCreator(
            output_path=output_path,
            path=path,
            sitename=_settings.get("SITENAME"),
            siteurl=_settings.get("SITEURL"),
        )
