from .appconfig import MB_VERSIONS
from django.utils.module_loading import import_string
from imagekit import ImageSpec
from imagekit.processors import ResizeToFill, ResizeToFit

import logging
logger = logging.getLogger(__name__)


version_specs = {}


def check_size_validity(width=None, height=None, max_width=None, max_height=None, **kwargs):
    assert not (width and not height), \
        "if you set width you have to set height"
    assert not (height and not width), \
        "if you set height you have to set width"
    assert not (max_width and not max_height), \
        "if you set max_width you have to set max_height"
    assert not (max_height and not max_width), \
        "if you set max_height you have to set max_width"
    assert not ((height and width) and (max_height and max_width)), \
        "(height,width) and (max_height max_width) assign one of thame"


for key, val in MB_VERSIONS.items():
    if val == "original":
        version_specs[key] = val
    else:
        if isinstance(val, str):
            try:
                Spec = import_string(val)
                version_specs[key] = Spec
            except:
                raise Exception(f"Invalid ImageSpec for: {key}")
        else:
            try:
                check_size_validity(**val)
                if (val.get("max_width") and val.get("max_height")):
                    resize = ResizeToFit(val['max_width'], val['max_height'])
                else:
                    resize = ResizeToFill(val['width'], val['height'])

                class Spec(ImageSpec):
                    processors = [resize]
                    options = val.get("options", None)
                    format = val.get('format', None)
                version_specs[key] = Spec
            except Exception as e:
                logger.critical(e)
                raise Exception(
                    f"Invalid options for: \"{key}\" in \"MEDIA_BROWSER_VERSIONS\"")
