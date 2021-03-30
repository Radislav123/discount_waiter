import scrapy


class ProjectItem(scrapy.Item):
    """Нужен как метка проекта."""
    pass


class FlexibleItem(ProjectItem):
    """Тестовый итем."""

    def __setitem__(self, key, value):
        if key not in self.fields:
            self.fields[key] = scrapy.Field()

        self._values[key] = value
