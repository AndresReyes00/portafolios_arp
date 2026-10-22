from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q


class Client(models.Model):
    name = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    address = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Unit(models.Model):

    class UnitType(models.TextChoices):
        DRY = "DRY", "Dry"
        REEFER = "REEFER", "Reefer"

    unit_number = models.CharField(
        max_length=30,
        unique=True,
    )

    vin = models.CharField(
        max_length=17,
        unique=True,
    )

    unit_type = models.CharField(
        max_length=10,
        choices=UnitType.choices,
    )

    last_fhwa = models.DateField(
        null=True,
        blank=True,
    )

    fhwa_interval_months = models.PositiveIntegerField(
        validators=[MinValueValidator(3)],
    )

    has_lg = models.BooleanField(default=False)

    last_lg_inspection = models.DateField(
        null=True,
        blank=True,
    )

    lg_interval_months = models.PositiveIntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(3)],
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="units",
    )

    class Meta:
        ordering = ["unit_number"]
        constraints = [
            models.CheckConstraint(
                condition=(
                    Q(has_lg=True)
                    | Q(
                        last_lg_inspection__isnull=True,
                        lg_interval_months__isnull=True,
                    )
                ),
                name="unit_without_lg_has_no_lg_schedule",
            ),
        ]

    def clean(self):
        super().clean()

        if self.has_lg:
            if self.lg_interval_months is None:
                raise ValidationError({
                    "lg_interval_months": (
                        "An LG inspection interval is required "
                        "when the unit has LG."
                    )
                })

        elif (
            self.last_lg_inspection is not None
            or self.lg_interval_months is not None
        ):
            raise ValidationError({
                "has_lg": (
                    "LG inspection data cannot be configured "
                    "when the unit does not have LG."
                )
            })

    def __str__(self):
        return self.unit_number


class Contact(models.Model):
    class ContactRole(models.TextChoices):
        OPERATIONS = "OPERATIONS", "Operations"
        MAINTENANCE = "MAINTENANCE", "Maintenance"
        INSPECTIONS = "INSPECTIONS", "Inspections"
        BILLING = "BILLING", "Billing"
        OTHER = "OTHER", "Other"

    client = models.ForeignKey(
        Client,
        on_delete=models.CASCADE,
        related_name="contacts",
    )

    name = models.CharField(max_length=150)

    phone = models.CharField(max_length=30)

    email = models.EmailField()

    role = models.CharField(
        max_length=20,
        choices=ContactRole.choices,
        default=ContactRole.OTHER,
    )

    class Meta:
        ordering = ["client__name", "name"]

    def __str__(self):
        return f"{self.name} - {self.client.name}"


class Vendor(models.Model):
    name = models.CharField(max_length=150)

    account_number = models.CharField(
        max_length=15,
        unique=True,
    )

    email = models.EmailField(
        blank=True,
    )

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} ({self.account_number})"


class VendorLocation(models.Model):
    vendor = models.ForeignKey(
        Vendor,
        on_delete=models.PROTECT,
        related_name="locations",
    )

    name = models.CharField(max_length=150)

    location = models.CharField(max_length=150)

    address = models.CharField(max_length=255)

    phone = models.CharField(
        max_length=30,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    class Meta:
        ordering = ["vendor__name", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["vendor", "name", "address"],
                name="unique_vendor_location",
            ),
        ]

    def __str__(self):
        return f"{self.vendor.name} - {self.name}"


class ClientVendorLocation(models.Model):
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="vendor_locations",
    )

    vendor_location = models.ForeignKey(
        VendorLocation,
        on_delete=models.PROTECT,
        related_name="client_assignments",
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = [
            "client__name",
            "vendor_location__vendor__name",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["client", "vendor_location"],
                name="unique_client_vendor_location",
            ),
        ]

    def __str__(self):
        return (
            f"{self.client.name} - "
            f"{self.vendor_location.vendor.name} - "
            f"{self.vendor_location.name}"
        )