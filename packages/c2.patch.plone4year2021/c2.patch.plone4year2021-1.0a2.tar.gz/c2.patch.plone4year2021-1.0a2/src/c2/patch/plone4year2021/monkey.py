from DateTime import DateTime

try:
    import pkg_resources

    plone_version = pkg_resources.get_distribution("Plone").version
    dot_count = plone_version.count(".")
    if dot_count > 1:
        major, minor, sub = plone_version.split(".", 2)
    else:
        major, minor = plone_version.split(".", 1)
        sub = "0"
    PLONE_VERSION = major
except:
    PLONE_VERSION = "0"

from logging import getLogger

logger = getLogger(__name__)
info = logger.info
info("Start monkey patching, Plone major version: %s", PLONE_VERSION)

if PLONE_VERSION == "4":
    try:
        from plone.app.form.widgets import datecomponents

        HAS_DATE_COMPONENTS = True
    except ImportError:
        HAS_DATE_COMPONENTS = False
    if HAS_DATE_COMPONENTS:
        datecomponents.PLONE_CEILING = DateTime(2050, 0)  # 2049-12-31
        info("patched: datecomponents supporting after 2021")
