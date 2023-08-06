import logging
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from google.oauth2 import service_account
from django.core.files.storage import default_storage
from datetime import datetime
from ..fields.encrypted_json import EncryptedJSONField
from .mappings import LAST_STATUS_CHOICES, STORAGE_PROVIDER_MAP

log = logging.getLogger(__name__)


class AbstractStorageTarget(models.Model):
    """Abstract implementation of a storage target which includes access details for how to interact with the downstream object storage system"""

    id = models.UUIDField(
        default=uuid4,
        primary_key=True,
        help_text=_("UUID identifying this objects"),
    )
    name = models.CharField(
        max_length=150,
        db_index=True,
        help_text=_("Name of this object"),
    )
    description = models.TextField(
        blank=True,
        null=True,
        help_text=_("Description of this object"),
    )
    last_checked = models.DateTimeField(
        null=True,
        blank=True,
        editable=False,
        help_text=_("Timestamp identifying when this storage provider was last checked"),
    )
    last_status = models.CharField(
        max_length=1,
        default="u",
        editable=False,
        choices=LAST_STATUS_CHOICES,
        help_text=_("Flag indiciating what the last status check result was"),
    )
    status_detail = models.TextField(
        blank=True,
        null=True,
        editable=False,
        help_text=_("Status details from last status check"),
    )
    provider = models.CharField(
        max_length=8,
        default="gcloud",
        choices=((k, v.get("name")) for k, v in STORAGE_PROVIDER_MAP.items()),
        help_text=_("Specific storage provider this target utilizes - generally an object storage solution of some sort"),
    )
    config = EncryptedJSONField(
        default=dict,
        blank=True,
        null=True,
        help_text=_("Key/value pairs to pass to the storage provider when initializing the storage backend"),
    )
    created = models.DateTimeField(
        auto_now_add=True,
        db_index=True,
        help_text=_("Timestamp indicating when this object was created"),
    )
    modified = models.DateTimeField(
        auto_now=True,
        db_index=True,
        help_text=_("Timestamp indicating when this object was last updated"),
    )
    as_of = models.DateTimeField(
        default=timezone.now,
        db_index=True,
        help_text=_("Timestamp that this storage provider should be used as of"),
    )

    @classmethod
    def as_of(cls, timestamp):
        return cls.objects.filter(as_of__lte=timestamp)

    def __self__(self):
        return "{} - {}".format(self.name, self.get_storage_provider_display())

    @property
    def storage_backend(self):
        """Property that should be used when assigning a DynamicStorageFileField's `storage` property at runtime"""
        if not getattr(self, "_storage_backend", None):
            if self.provider != "default":
                create_class = STORAGE_PROVIDER_MAP[self.provider]["class"]
                create_kwargs = getattr(self, "config", {}).copy()
                if self.provider == "gcloud":
                    log.debug("Initializing Google Cloud Storage backend")
                    create_kwargs["credentials"] = service_account.Credentials.from_service_account_info(create_kwargs.pop("credentials", {}))
                elif self.provider == "digitalocean":
                    log.debug("Initializing DigitalOcean storage backend")
                    create_kwargs["addressing_style"] = "path"
                    if not create_kwargs.get("region_name"):
                        create_kwargs["region_name"] = "SFO1"
                    create_kwargs["endpoint_url"] = "https://{}.digitaloceanspaces.com".format(create_kwargs.get("region_name", "SFO1"))
                elif self.provider == "s3boto3":
                    log.debug("Initializing AWS/S3Boto3 storage backend")
                    create_kwargs["default_acl"] = create_kwargs.get("default_acl", "bucket-owner-full-control")
                else:
                    log.debug("Initializing {} storage backend".format(self.provider))
                self._storage_backend = create_class(**create_kwargs)
            else:
                log.debug("Storage provider is set to default - assigning Django default_storage backend")
                self._storage_backend = default_storage
        return self._storage_backend

    @storage_backend.setter
    def storage_backend(self, val):
        self._storage_backend = val

    def _check_credentials(self):
        s = datetime.utcnow()
        ret_val = {"checked_at": s.isoformat()}
        if self.provider == "gcloud":
            ret_val["available"] = True if self.storage_backend.client.lookup_bucket(self.storage_backend.bucket_name) else False
        elif self.provider == "s3boto3":
            pass
        else:
            ret_val.update({"location": default_storage.location, "base_url": default_storage.base_url, "available": True if default_storage.get_available_name("") else False})
        ret_val["elapsed"] = (datetime.utcnow() - s).total_seconds()
        return ret_val

    class Meta:
        abstract = True
        verbose_name = _("Storage Target")
        verbose_name_plural = _("Storage Targets")
