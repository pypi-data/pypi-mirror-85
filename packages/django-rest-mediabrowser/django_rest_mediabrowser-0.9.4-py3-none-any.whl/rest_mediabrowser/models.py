from django.dispatch import receiver
from django.db.models.signals import pre_delete
import os
import shutil
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from taggit.managers import TaggableManager
from .appconfig import MB_STORAGE, MB_THUMBNAIL_FORMAT, MB_PUBLISHED_FILE_PATH, MB_VERSIONS_ROOT, MB_ROOT, MB_PUBLISHED_ROOT
from .specs import version_specs
from django.urls import reverse
from imagekit import ImageSpec
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from PIL import Image
from django.core.files.base import ContentFile
import logging
from pathlib import Path
from urllib.parse import urljoin
# Create your models here.
from django.utils.module_loading import import_string

logger = logging.getLogger(__name__)

PERMISSION_LEVELS = (('e', 'Edit'),
                     ('v', 'View'),)


def image_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/images/{1}'.format(instance.owner.id, filename)


def image_thumbnail_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/thumbnails/{1}'.format(instance.owner.id, filename)


def file_upload_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/files/{1}'.format(instance.owner.id, filename)


def delete_version_image(instance):
    if(not instance.versions):
        return
    for version in instance.versions:
        full_path = f"{MB_VERSIONS_ROOT}/{instance.versions[version]}"
        try:
            os.remove(full_path, exist_ok=True)
        except Exception as error:
            logger.critical(error)
    instance.versions = None


class Thumbnail(ImageSpec):
    processors = [ResizeToFill(200, 200)]
    format = MB_THUMBNAIL_FORMAT
    options = {'quality': 90}


class Collection(models.Model):
    """
    A collection to share in with ease
    """
    name = models.CharField(_("name"), max_length=500)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=_("user"),
                              related_name="collections",
                              on_delete=models.CASCADE)

    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_(
        "shared_with"), related_name="shared_collections", through="rest_mediabrowser.CollectionPermission")

    def __str__(self):
        return f'{self.name}'


class MediaImage(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=_("owner"),
                              related_name="media_images",
                              on_delete=models.CASCADE)
    collection = models.ForeignKey("rest_mediabrowser.Collection",
                                   verbose_name=_("collection"),
                                   related_name="image_files",
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    tags = TaggableManager(blank=True)
    description = models.CharField(
        _("description"), max_length=500, blank=True)
    alt_text = models.CharField(
        _("alternative text"), max_length=100, blank=True)
    height = models.IntegerField(_("height"), blank=True, null=True)
    width = models.IntegerField(_("width"), blank=True, null=True)
    image = models.ImageField(_("image"), upload_to=image_upload_path,
                              height_field='height', width_field='width', max_length=500, storage=MB_STORAGE)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_(
        "shared_with"), related_name="shared_images", through="rest_mediabrowser.ImagePermission")
    published = models.BooleanField(_("Status"), default=False)
    thumbnail = models.ImageField(_("Thumbnail"), upload_to=image_thumbnail_path,
                                  max_length=500, storage=MB_STORAGE, null=True, blank=True)
    extension = models.CharField(_("Extension"), max_length=50, blank=True)
    published_path = models.CharField(
        _("Published Path"), max_length=500, blank=True)
    versions = models.JSONField(null=True, blank=True)

    def __init__(self, *args, **kwargs):
        super(MediaImage, self).__init__(*args, **kwargs)
        self.prev_image_name = self.image.name if self.image else ''
        self.prev_published = self.published

    def save(self, *args, **kwargs):
        if self.image:
            if not self.id or self.image.name != self.prev_image_name:
                delete_version_image(self)
                self.generate_thumbnail(save=False)
                self.extension = self.image.name.split('.')[-1]
            if self.prev_published and not self.published:
                delete_version_image(self)
            # if self.published != self.prev_published or self.image.name != self.prev_image_name:
            #     dest = os.path.join(MB_PUBLISHED_FILE_PATH, self.image.name)
            #     if self.published:
            #         os.makedirs("/".join(dest.split('/')[:-1]), exist_ok=True)
            #         shutil.copy(os.path.join(MB_ROOT, self.image.name),
            #                    dest)
            #         self.published_path = os.path.join(
            #             settings.MEDIA_URL, MB_PUBLISHED_ROOT, self.image.name)
            #     else:
            #         logger.critical(dest)
            #         self.published_path = ""
            #         if Path(dest).is_file():
            #             logger.critical("IS_FILE")
            #             os.remove(dest)
        super(MediaImage, self).save(*args, **kwargs)

    def generate_thumbnail(self, save=True):
        image_generator = Thumbnail(source=self.image)
        result = image_generator.generate()
        thumb_file = ContentFile(result.getvalue())
        self.thumbnail.save(
            f'thumbnail.{MB_THUMBNAIL_FORMAT.lower()}', thumb_file, False)
        if save:
            self.save()

    def get_version(self, version_spec="original"):
        if self.published:
            if version_spec == "original":
                return self.published_path
            else:
                # Check version existance
                SpecClass = version_specs.get(version_spec, None)
                if SpecClass is None:
                    raise Exception(
                        f"No such version \"{version_spec}\" specified in \"MEDIA_BROWSER_VERSIONS\"")
                # return path if version exist
                if self.versions and self.versions.get(version_spec):
                    return self.versions[version_spec]
                else:
                    # assign format
                    if SpecClass.format is None:
                        SpecClass.format = self.extension
                    # Assign path
                    relative_path = self.image.url.split("/")
                    file_name = f"{relative_path[-1].split('.')[0]}.{SpecClass.format}"
                    relative_path[-1] = f"versions/{version_spec}-{file_name}"
                    relative_path = "/".join(relative_path[1:])
                    full_path = f"{MB_VERSIONS_ROOT}/{relative_path}"
                    # Create dir if needed
                    full_path_obj = Path(full_path)
                    os.makedirs(full_path_obj.parent, exist_ok=True)
                    # Start conversion
                    image_generator = SpecClass(source=self.image)
                    result = image_generator.generate()
                    with open(full_path, 'wb') as ofile:
                        ofile.write(result.read())
                    # update version data
                    if(not self.versions):
                        self.versions = {}
                    self.versions[version_spec] = relative_path
                    self.save()
                    return relative_path
                # else:
                #     SpecClass = version_specs.get(version_spec, None)
                #     if SpecClass is None:
                #         raise Exception("No such version specification")
                #     if SpecClass.format is None:
                #         SpecClass.format = self.extension
                #     path_parts = self.image.path.split("/")
                #     logger.critical(f"{path_parts}--{new_path_parts}")
                #     file_name = f"{path_parts[-1].split('.')[0]}.{SpecClass.format}"
                #     path_parts[-1] = file_name
                #     path_parts.insert(-1, f"versions/{version_spec}")
                #     dest = "/".join(path_parts)
                #     logger.critical(f"--{dest}--{file_name}")
                #     path = Path(dest)
                #     if path.is_file():
                #         return dest
                #     else:
                #         os.makedirs(path.parent, exist_ok=True)
                #         image_generator = SpecClass(source=self.image)
                #         result = image_generator.generate()
                #         with open(dest, 'wb') as ofile:
                #             ofile.write(result.read())
                #         return dest
        else:
            raise Exception("This asset is not published")

    @property
    def ext(self):
        return self.extension if self.extension else self.image.name.split('.')[-1]

    def get_image_url(self):
        return reverse("mb-image", kwargs={"pk": self.pk, "ext": self.ext})

    def get_thumbnail_url(self):
        return reverse("mb-thumbnail", kwargs={"pk": self.pk, 'ext': MB_THUMBNAIL_FORMAT.lower()})

    def __str__(self):
        return f'{self.id}-{self.description}'


@receiver(pre_delete, sender=MediaImage)
def deleted_mediaimage(sender, instance, using, **kwargs):
    delete_version_image(instance)


class MediaFile(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              verbose_name=_("owner"),
                              related_name="media_files",
                              on_delete=models.CASCADE)
    collection = models.ForeignKey("rest_mediabrowser.Collection",
                                   verbose_name=_("collection"),
                                   related_name="media_files",
                                   on_delete=models.SET_NULL,
                                   null=True, blank=True)
    tags = TaggableManager()
    description = models.CharField(
        _("description"), max_length=500, blank=True)
    file = models.FileField(
        _("file"), upload_to=file_upload_path, max_length=500, storage=MB_STORAGE)
    shared_with = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name=_(
        "shared_with"), related_name="shared_files", through="rest_mediabrowser.FilePermission")
    published = models.BooleanField(_("Status"), default=False)
    extension = models.CharField(_("Extension"), max_length=50, blank=True)
    published_path = models.CharField(
        _("Published Path"), max_length=500, blank=True)

    def __init__(self, *args, **kwargs):
        super(MediaFile, self).__init__(*args, **kwargs)
        self.prev_file_name = self.file.name if self.file else ''
        self.prev_published = self.published

    def save(self, *args, **kwargs):
        if self.file:
            if self.file.name != self.prev_file_name:
                self.extension = self.file.name.split('.')[-1]
            # if self.published != self.prev_published or self.file.name != self.prev_file_name:
            #     dest = os.path.join(MB_PUBLISHED_FILE_PATH, self.file.name)
            #     if self.published:
            #         os.makedirs("/".join(dest.split('/')[:-1]), exist_ok=True)
            #         os.symlink(os.path.join(MB_ROOT, self.file.name),
            #                    dest)
            #         self.published_path = os.path.join(
            #             settings.MEDIA_URL, MB_PUBLISHED_ROOT, self.file.name)
            #     else:
            #         self.published_path = ""
            #         if Path(dest).is_file():
            #             os.unlink(dest)
        super(MediaFile, self).save(*args, **kwargs)

    @property
    def ext(self):
        return self.extension if self.extension else self.file.name.split('.')[-1]

    def get_file_url(self):
        return reverse("mb-file", kwargs={"pk": self.pk, "ext": self.ext})

    def __str__(self):
        return f'{self.id}-{self.description}'


class ImagePermission(models.Model):
    image = models.ForeignKey(
        "rest_mediabrowser.MediaImage", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    permission = models.CharField(
        _("permission"), max_length=2, choices=PERMISSION_LEVELS)\


    class Meta:
        unique_together = (("user", "image"),)


class FilePermission(models.Model):
    file = models.ForeignKey(
        "rest_mediabrowser.MediaFile", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    permission = models.CharField(
        _("permission"), max_length=2, choices=PERMISSION_LEVELS)

    class Meta:
        unique_together = (("user", "file"),)


class CollectionPermission(models.Model):
    collection = models.ForeignKey(
        "rest_mediabrowser.Collection", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    permission = models.CharField(
        _("permission"), max_length=2, choices=PERMISSION_LEVELS)

    class Meta:
        unique_together = (("user", "collection"),)
