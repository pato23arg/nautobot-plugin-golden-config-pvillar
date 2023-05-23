"""Forms for Device Configuration Backup."""
# pylint: disable=too-many-ancestors

from django import forms

import nautobot.extras.forms as extras_forms
import nautobot.utilities.forms as utilities_forms
from nautobot.dcim.models import Device, Platform, Region, Site, DeviceRole, DeviceType, Manufacturer, Rack, RackGroup
from nautobot.extras.models import Status, GitRepository, DynamicGroup
from nautobot.tenancy.models import Tenant, TenantGroup
from nautobot.utilities.forms import SlugField
from nautobot.extras.forms import NautobotFilterForm, NautobotBulkEditForm, NautobotModelForm


from nautobot_golden_config import models

# ConfigCompliance


class ConfigComplianceFilterForm(NautobotFilterForm):
    """Filter Form for ConfigCompliance instances."""

    model = models.ConfigCompliance
    # Set field order to be explicit
    field_order = [
        "q",
        "tenant_group",
        "tenant",
        "region",
        "site",
        "rack_group_id",
        "rack_id",
        "role",
        "manufacturer",
        "platform",
        "device_status",
        "device_type_id",
        "device_id",
    ]

    q = forms.CharField(required=False, label="Search")
    tenant_group = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=TenantGroup.objects.all(), to_field_name="slug", required=False, null_option="None"
    )
    tenant = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=Tenant.objects.all(),
        to_field_name="slug",
        required=False,
        null_option="None",
        query_params={"group": "$tenant_group"},
    )
    region = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=Region.objects.all(), to_field_name="slug", required=False
    )
    site = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=Site.objects.all(), to_field_name="slug", required=False, query_params={"region": "$region"}
    )
    rack_group_id = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=RackGroup.objects.all(), required=False, label="Rack group", query_params={"site": "$site"}
    )
    rack_id = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=Rack.objects.all(),
        required=False,
        label="Rack",
        null_option="None",
        query_params={
            "site": "$site",
            "group_id": "$rack_group_id",
        },
    )
    role = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=DeviceRole.objects.all(), to_field_name="slug", required=False
    )
    manufacturer = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=Manufacturer.objects.all(), to_field_name="slug", required=False, label="Manufacturer"
    )
    device_type_id = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=DeviceType.objects.all(),
        required=False,
        label="Model",
        display_field="model",
        query_params={"manufacturer": "$manufacturer"},
    )

    platform = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=Platform.objects.all(), to_field_name="slug", required=False, null_option="None"
    )
    device_id = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=Device.objects.all(), required=False, null_option="None", label="Device"
    )

    def __init__(self, *args, **kwargs):
        """Required for status to work."""
        super().__init__(*args, **kwargs)
        self.fields["device_status"] = utilities_forms.DynamicModelMultipleChoiceField(
            required=False,
            queryset=Status.objects.all(),
            query_params={"content_types": Device._meta.label_lower},
            display_field="label",
            label="Device Status",
            to_field_name="slug",
        )
        self.order_fields(self.field_order)  # Reorder fields again


# ComplianceRule


class ComplianceRuleForm(NautobotModelForm):
    """Filter Form for ComplianceRule instances."""

    platform = utilities_forms.DynamicModelChoiceField(queryset=Platform.objects.all())

    class Meta:
        """Boilerplate form Meta data for compliance rule."""

        model = models.ComplianceRule
        fields = (
            "platform",
            "feature",
            "description",
            "config_ordered",
            "match_config",
            "config_type",
            # "remediation_setting",
        )


class ComplianceRuleFilterForm(NautobotFilterForm):
    """Form for ComplianceRule instances."""

    model = models.ComplianceRule

    q = forms.CharField(required=False, label="Search")
    platform = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=Platform.objects.all(), to_field_name="slug", required=False, null_option="None"
    )

    feature = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=models.ComplianceFeature.objects.all(), required=False
    )


class ComplianceRuleBulkEditForm(NautobotBulkEditForm):
    """BulkEdit form for ComplianceRule instances."""

    pk = forms.ModelMultipleChoiceField(queryset=models.ComplianceRule.objects.all(), widget=forms.MultipleHiddenInput)

    class Meta:
        """Boilerplate form Meta data for ComplianceRule."""

        nullable_fields = []


class ComplianceRuleCSVForm(extras_forms.CustomFieldModelCSVForm):
    """CSV Form for ComplianceRule instances."""

    class Meta:
        """Boilerplate form Meta data for ComplianceRule."""

        model = models.ComplianceRule
        fields = models.ComplianceRule.csv_headers


# ComplianceFeature


class ComplianceFeatureForm(NautobotModelForm):
    """Filter Form for ComplianceFeature instances."""

    slug = SlugField()

    class Meta:
        """Boilerplate form Meta data for compliance feature."""

        model = models.ComplianceFeature
        fields = ("name", "slug", "description")


class ComplianceFeatureFilterForm(NautobotFilterForm):
    """Form for ComplianceFeature instances."""

    model = models.ComplianceFeature
    q = forms.CharField(required=False, label="Search")
    name = utilities_forms.DynamicModelChoiceField(queryset=models.ComplianceFeature.objects.all(), required=False)


class ComplianceFeatureBulkEditForm(NautobotBulkEditForm):
    """BulkEdit form for ComplianceFeature instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.ComplianceFeature.objects.all(), widget=forms.MultipleHiddenInput
    )

    class Meta:
        """Boilerplate form Meta data for ComplianceFeature."""

        nullable_fields = []


class ComplianceFeatureCSVForm(extras_forms.CustomFieldModelCSVForm):
    """CSV Form for ComplianceFeature instances."""

    class Meta:
        """Boilerplate form Meta data for ComplianceFeature."""

        model = models.ComplianceFeature
        fields = models.ComplianceFeature.csv_headers


# ConfigRemove


class ConfigRemoveForm(NautobotModelForm):
    """Filter Form for Line Removal instances."""

    platform = utilities_forms.DynamicModelChoiceField(queryset=Platform.objects.all())

    class Meta:
        """Boilerplate form Meta data for removal feature."""

        model = models.ConfigRemove
        fields = (
            "platform",
            "name",
            "description",
            "regex",
        )


class ConfigRemoveFilterForm(NautobotFilterForm):
    """Filter Form for Line Removal."""

    model = models.ConfigRemove
    platform = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=Platform.objects.all(), to_field_name="slug", required=False, null_option="None"
    )
    name = utilities_forms.DynamicModelChoiceField(
        queryset=models.ConfigRemove.objects.all(), to_field_name="name", required=False
    )


class ConfigRemoveBulkEditForm(NautobotBulkEditForm):
    """BulkEdit form for ConfigRemove instances."""

    pk = forms.ModelMultipleChoiceField(queryset=models.ConfigRemove.objects.all(), widget=forms.MultipleHiddenInput)

    class Meta:
        """Boilerplate form Meta data for ConfigRemove."""

        nullable_fields = []


class ConfigRemoveCSVForm(extras_forms.CustomFieldModelCSVForm):
    """CSV Form for ConfigRemove instances."""

    class Meta:
        """Boilerplate form Meta data for ConfigRemove."""

        model = models.ConfigRemove
        fields = models.ConfigRemove.csv_headers


# ConfigReplace


class ConfigReplaceForm(NautobotModelForm):
    """Filter Form for Line Removal instances."""

    platform = utilities_forms.DynamicModelChoiceField(queryset=Platform.objects.all())

    class Meta:
        """Boilerplate form Meta data for removal feature."""

        model = models.ConfigReplace
        fields = (
            "platform",
            "name",
            "description",
            "regex",
            "replace",
        )


class ConfigReplaceFilterForm(NautobotFilterForm):
    """Filter Form for Line Replacement."""

    model = models.ConfigReplace

    platform = utilities_forms.DynamicModelMultipleChoiceField(
        queryset=Platform.objects.all(), to_field_name="slug", required=False, null_option="None"
    )
    name = utilities_forms.DynamicModelChoiceField(
        queryset=models.ConfigReplace.objects.all(), to_field_name="name", required=False
    )


class ConfigReplaceCSVForm(extras_forms.CustomFieldModelCSVForm):
    """CSV Form for ConfigReplace instances."""

    class Meta:
        """Boilerplate form Meta data for ConfigReplace."""

        model = models.ConfigReplace
        fields = models.ConfigReplace.csv_headers


class ConfigReplaceBulkEditForm(NautobotBulkEditForm):
    """BulkEdit form for ConfigReplace instances."""

    pk = forms.ModelMultipleChoiceField(queryset=models.ConfigReplace.objects.all(), widget=forms.MultipleHiddenInput)

    class Meta:
        """Boilerplate form Meta data for ConfigReplace."""

        nullable_fields = []


# GoldenConfigSetting


class GoldenConfigSettingForm(NautobotModelForm):
    """Filter Form for GoldenConfigSettingForm instances."""

    slug = SlugField()
    dynamic_group = utilities_forms.DynamicModelChoiceField(queryset=DynamicGroup.objects.all(), required=False)

    class Meta:
        """Filter Form Meta Data for GoldenConfigSettingForm instances."""

        model = models.GoldenConfigSetting
        fields = (
            "name",
            "slug",
            "weight",
            "description",
            "backup_repository",
            "backup_path_template",
            "intended_repository",
            "intended_path_template",
            "jinja_repository",
            "jinja_path_template",
            "backup_test_connectivity",
            "dynamic_group",
            "sot_agg_query",
            "tags",
        )


class GoldenConfigSettingFilterForm(NautobotFilterForm):
    """Form for GoldenConfigSetting instances."""

    model = models.GoldenConfigSetting

    q = forms.CharField(required=False, label="Search")
    name = forms.CharField(required=False)
    weight = forms.IntegerField(required=False)
    backup_repository = forms.ModelChoiceField(
        queryset=GitRepository.objects.filter(provided_contents__contains="nautobot_golden_config.backupconfigs"),
        required=False,
    )
    intended_repository = forms.ModelChoiceField(
        queryset=GitRepository.objects.filter(provided_contents__contains="nautobot_golden_config.intendedconfigs"),
        required=False,
    )
    jinja_repository = forms.ModelChoiceField(
        queryset=GitRepository.objects.filter(provided_contents__contains="nautobot_golden_config.jinjatemplate"),
        required=False,
    )


class GoldenConfigSettingCSVForm(extras_forms.CustomFieldModelCSVForm):
    """CSV Form for GoldenConfigSetting instances."""

    class Meta:
        """Boilerplate form Meta data for GoldenConfigSetting."""

        model = models.GoldenConfigSetting
        fields = models.GoldenConfigSetting.csv_headers


class GoldenConfigSettingBulkEditForm(NautobotBulkEditForm):
    """BulkEdit form for GoldenConfigSetting instances."""

    pk = forms.ModelMultipleChoiceField(
        queryset=models.GoldenConfigSetting.objects.all(), widget=forms.MultipleHiddenInput
    )

    class Meta:
        """Boilerplate form Meta data for GoldenConfigSetting."""

        nullable_fields = []


# Remediation Setting
class RemediationSettingForm(NautobotModelForm):
    """Filter Form for Line Removal instances."""

    class Meta:
        """Boilerplate form Meta data for removal feature."""

        model = models.RemediationSetting
        fields = (
            "platform",
            "remediation_type",
            "remediation_options",
        )


class RemediationSettingFilterForm(NautobotFilterForm):
    """Filter Form for Line Replacement."""

    model = models.RemediationSetting


class RemediationSettingCSVForm(extras_forms.CustomFieldModelCSVForm):
    """CSV Form for RemediationSetting instances."""

    class Meta:
        """Boilerplate form Meta data for RemediationSetting."""

        model = models.RemediationSetting
        fields = models.RemediationSetting.csv_headers


class RemediationSettingBulkEditForm(NautobotBulkEditForm):
    """BulkEdit form for RemediationSetting instances."""

    pk = forms.ModelMultipleChoiceField(queryset=models.RemediationSetting.objects.all(), widget=forms.MultipleHiddenInput)

    class Meta:
        """Boilerplate form Meta data for RemediationSetting."""

        nullable_fields = []
