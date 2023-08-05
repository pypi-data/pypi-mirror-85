# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: google/ads/googleads_v4/proto/resources/invoice.proto

import sys
_b=sys.version_info[0]<3 and (lambda x:x) or (lambda x:x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from google.ads.google_ads.v4.proto.common import dates_pb2 as google_dot_ads_dot_googleads__v4_dot_proto_dot_common_dot_dates__pb2
from google.ads.google_ads.v4.proto.enums import invoice_type_pb2 as google_dot_ads_dot_googleads__v4_dot_proto_dot_enums_dot_invoice__type__pb2
from google.api import field_behavior_pb2 as google_dot_api_dot_field__behavior__pb2
from google.api import resource_pb2 as google_dot_api_dot_resource__pb2
from google.protobuf import wrappers_pb2 as google_dot_protobuf_dot_wrappers__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2


DESCRIPTOR = _descriptor.FileDescriptor(
  name='google/ads/googleads_v4/proto/resources/invoice.proto',
  package='google.ads.googleads.v4.resources',
  syntax='proto3',
  serialized_options=_b('\n%com.google.ads.googleads.v4.resourcesB\014InvoiceProtoP\001ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v4/resources;resources\242\002\003GAA\252\002!Google.Ads.GoogleAds.V4.Resources\312\002!Google\\Ads\\GoogleAds\\V4\\Resources\352\002%Google::Ads::GoogleAds::V4::Resources'),
  serialized_pb=_b('\n5google/ads/googleads_v4/proto/resources/invoice.proto\x12!google.ads.googleads.v4.resources\x1a\x30google/ads/googleads_v4/proto/common/dates.proto\x1a\x36google/ads/googleads_v4/proto/enums/invoice_type.proto\x1a\x1fgoogle/api/field_behavior.proto\x1a\x19google/api/resource.proto\x1a\x1egoogle/protobuf/wrappers.proto\x1a\x1cgoogle/api/annotations.proto\"\xcb\x0e\n\x07Invoice\x12?\n\rresource_name\x18\x01 \x01(\tB(\xe0\x41\x03\xfa\x41\"\n googleads.googleapis.com/Invoice\x12-\n\x02id\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12M\n\x04type\x18\x03 \x01(\x0e\x32:.google.ads.googleads.v4.enums.InvoiceTypeEnum.InvoiceTypeB\x03\xe0\x41\x03\x12\x38\n\rbilling_setup\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12>\n\x13payments_account_id\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12>\n\x13payments_profile_id\x18\x06 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12\x35\n\nissue_date\x18\x07 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12\x33\n\x08\x64ue_date\x18\x08 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12J\n\x12service_date_range\x18\t \x01(\x0b\x32).google.ads.googleads.v4.common.DateRangeB\x03\xe0\x41\x03\x12\x38\n\rcurrency_code\x18\n \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12J\n invoice_level_adjustments_micros\x18\x0b \x01(\x0b\x32\x1b.google.protobuf.Int64ValueB\x03\xe0\x41\x03\x12@\n\x16subtotal_amount_micros\x18\x0c \x01(\x0b\x32\x1b.google.protobuf.Int64ValueB\x03\xe0\x41\x03\x12;\n\x11tax_amount_micros\x18\r \x01(\x0b\x32\x1b.google.protobuf.Int64ValueB\x03\xe0\x41\x03\x12=\n\x13total_amount_micros\x18\x0e \x01(\x0b\x32\x1b.google.protobuf.Int64ValueB\x03\xe0\x41\x03\x12<\n\x11\x63orrected_invoice\x18\x0f \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12<\n\x11replaced_invoices\x18\x10 \x03(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12\x32\n\x07pdf_url\x18\x11 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12\x66\n\x18\x61\x63\x63ount_budget_summaries\x18\x12 \x03(\x0b\x32?.google.ads.googleads.v4.resources.Invoice.AccountBudgetSummaryB\x03\xe0\x41\x03\x1a\xe2\x04\n\x14\x41\x63\x63ountBudgetSummary\x12\x33\n\x08\x63ustomer\x18\x01 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12\x44\n\x19\x63ustomer_descriptive_name\x18\x02 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12\x39\n\x0e\x61\x63\x63ount_budget\x18\x03 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12>\n\x13\x61\x63\x63ount_budget_name\x18\x04 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12@\n\x15purchase_order_number\x18\x05 \x01(\x0b\x32\x1c.google.protobuf.StringValueB\x03\xe0\x41\x03\x12@\n\x16subtotal_amount_micros\x18\x06 \x01(\x0b\x32\x1b.google.protobuf.Int64ValueB\x03\xe0\x41\x03\x12;\n\x11tax_amount_micros\x18\x07 \x01(\x0b\x32\x1b.google.protobuf.Int64ValueB\x03\xe0\x41\x03\x12=\n\x13total_amount_micros\x18\x08 \x01(\x0b\x32\x1b.google.protobuf.Int64ValueB\x03\xe0\x41\x03\x12T\n\x1c\x62illable_activity_date_range\x18\t \x01(\x0b\x32).google.ads.googleads.v4.common.DateRangeB\x03\xe0\x41\x03:N\xea\x41K\n googleads.googleapis.com/Invoice\x12\'customers/{customer}/invoices/{invoice}B\xf9\x01\n%com.google.ads.googleads.v4.resourcesB\x0cInvoiceProtoP\x01ZJgoogle.golang.org/genproto/googleapis/ads/googleads/v4/resources;resources\xa2\x02\x03GAA\xaa\x02!Google.Ads.GoogleAds.V4.Resources\xca\x02!Google\\Ads\\GoogleAds\\V4\\Resources\xea\x02%Google::Ads::GoogleAds::V4::Resourcesb\x06proto3')
  ,
  dependencies=[google_dot_ads_dot_googleads__v4_dot_proto_dot_common_dot_dates__pb2.DESCRIPTOR,google_dot_ads_dot_googleads__v4_dot_proto_dot_enums_dot_invoice__type__pb2.DESCRIPTOR,google_dot_api_dot_field__behavior__pb2.DESCRIPTOR,google_dot_api_dot_resource__pb2.DESCRIPTOR,google_dot_protobuf_dot_wrappers__pb2.DESCRIPTOR,google_dot_api_dot_annotations__pb2.DESCRIPTOR,])




_INVOICE_ACCOUNTBUDGETSUMMARY = _descriptor.Descriptor(
  name='AccountBudgetSummary',
  full_name='google.ads.googleads.v4.resources.Invoice.AccountBudgetSummary',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='customer', full_name='google.ads.googleads.v4.resources.Invoice.AccountBudgetSummary.customer', index=0,
      number=1, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='customer_descriptive_name', full_name='google.ads.googleads.v4.resources.Invoice.AccountBudgetSummary.customer_descriptive_name', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_budget', full_name='google.ads.googleads.v4.resources.Invoice.AccountBudgetSummary.account_budget', index=2,
      number=3, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_budget_name', full_name='google.ads.googleads.v4.resources.Invoice.AccountBudgetSummary.account_budget_name', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='purchase_order_number', full_name='google.ads.googleads.v4.resources.Invoice.AccountBudgetSummary.purchase_order_number', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='subtotal_amount_micros', full_name='google.ads.googleads.v4.resources.Invoice.AccountBudgetSummary.subtotal_amount_micros', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tax_amount_micros', full_name='google.ads.googleads.v4.resources.Invoice.AccountBudgetSummary.tax_amount_micros', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='total_amount_micros', full_name='google.ads.googleads.v4.resources.Invoice.AccountBudgetSummary.total_amount_micros', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='billable_activity_date_range', full_name='google.ads.googleads.v4.resources.Invoice.AccountBudgetSummary.billable_activity_date_range', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[],
  enum_types=[
  ],
  serialized_options=None,
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=1498,
  serialized_end=2108,
)

_INVOICE = _descriptor.Descriptor(
  name='Invoice',
  full_name='google.ads.googleads.v4.resources.Invoice',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
    _descriptor.FieldDescriptor(
      name='resource_name', full_name='google.ads.googleads.v4.resources.Invoice.resource_name', index=0,
      number=1, type=9, cpp_type=9, label=1,
      has_default_value=False, default_value=_b("").decode('utf-8'),
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003\372A\"\n googleads.googleapis.com/Invoice'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='id', full_name='google.ads.googleads.v4.resources.Invoice.id', index=1,
      number=2, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='type', full_name='google.ads.googleads.v4.resources.Invoice.type', index=2,
      number=3, type=14, cpp_type=8, label=1,
      has_default_value=False, default_value=0,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='billing_setup', full_name='google.ads.googleads.v4.resources.Invoice.billing_setup', index=3,
      number=4, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payments_account_id', full_name='google.ads.googleads.v4.resources.Invoice.payments_account_id', index=4,
      number=5, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='payments_profile_id', full_name='google.ads.googleads.v4.resources.Invoice.payments_profile_id', index=5,
      number=6, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='issue_date', full_name='google.ads.googleads.v4.resources.Invoice.issue_date', index=6,
      number=7, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='due_date', full_name='google.ads.googleads.v4.resources.Invoice.due_date', index=7,
      number=8, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='service_date_range', full_name='google.ads.googleads.v4.resources.Invoice.service_date_range', index=8,
      number=9, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='currency_code', full_name='google.ads.googleads.v4.resources.Invoice.currency_code', index=9,
      number=10, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='invoice_level_adjustments_micros', full_name='google.ads.googleads.v4.resources.Invoice.invoice_level_adjustments_micros', index=10,
      number=11, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='subtotal_amount_micros', full_name='google.ads.googleads.v4.resources.Invoice.subtotal_amount_micros', index=11,
      number=12, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='tax_amount_micros', full_name='google.ads.googleads.v4.resources.Invoice.tax_amount_micros', index=12,
      number=13, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='total_amount_micros', full_name='google.ads.googleads.v4.resources.Invoice.total_amount_micros', index=13,
      number=14, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='corrected_invoice', full_name='google.ads.googleads.v4.resources.Invoice.corrected_invoice', index=14,
      number=15, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='replaced_invoices', full_name='google.ads.googleads.v4.resources.Invoice.replaced_invoices', index=15,
      number=16, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='pdf_url', full_name='google.ads.googleads.v4.resources.Invoice.pdf_url', index=16,
      number=17, type=11, cpp_type=10, label=1,
      has_default_value=False, default_value=None,
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
    _descriptor.FieldDescriptor(
      name='account_budget_summaries', full_name='google.ads.googleads.v4.resources.Invoice.account_budget_summaries', index=17,
      number=18, type=11, cpp_type=10, label=3,
      has_default_value=False, default_value=[],
      message_type=None, enum_type=None, containing_type=None,
      is_extension=False, extension_scope=None,
      serialized_options=_b('\340A\003'), file=DESCRIPTOR),
  ],
  extensions=[
  ],
  nested_types=[_INVOICE_ACCOUNTBUDGETSUMMARY, ],
  enum_types=[
  ],
  serialized_options=_b('\352AK\n googleads.googleapis.com/Invoice\022\'customers/{customer}/invoices/{invoice}'),
  is_extendable=False,
  syntax='proto3',
  extension_ranges=[],
  oneofs=[
  ],
  serialized_start=321,
  serialized_end=2188,
)

_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['customer'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['customer_descriptive_name'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['account_budget'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['account_budget_name'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['purchase_order_number'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['subtotal_amount_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['tax_amount_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['total_amount_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['billable_activity_date_range'].message_type = google_dot_ads_dot_googleads__v4_dot_proto_dot_common_dot_dates__pb2._DATERANGE
_INVOICE_ACCOUNTBUDGETSUMMARY.containing_type = _INVOICE
_INVOICE.fields_by_name['id'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE.fields_by_name['type'].enum_type = google_dot_ads_dot_googleads__v4_dot_proto_dot_enums_dot_invoice__type__pb2._INVOICETYPEENUM_INVOICETYPE
_INVOICE.fields_by_name['billing_setup'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE.fields_by_name['payments_account_id'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE.fields_by_name['payments_profile_id'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE.fields_by_name['issue_date'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE.fields_by_name['due_date'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE.fields_by_name['service_date_range'].message_type = google_dot_ads_dot_googleads__v4_dot_proto_dot_common_dot_dates__pb2._DATERANGE
_INVOICE.fields_by_name['currency_code'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE.fields_by_name['invoice_level_adjustments_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_INVOICE.fields_by_name['subtotal_amount_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_INVOICE.fields_by_name['tax_amount_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_INVOICE.fields_by_name['total_amount_micros'].message_type = google_dot_protobuf_dot_wrappers__pb2._INT64VALUE
_INVOICE.fields_by_name['corrected_invoice'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE.fields_by_name['replaced_invoices'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE.fields_by_name['pdf_url'].message_type = google_dot_protobuf_dot_wrappers__pb2._STRINGVALUE
_INVOICE.fields_by_name['account_budget_summaries'].message_type = _INVOICE_ACCOUNTBUDGETSUMMARY
DESCRIPTOR.message_types_by_name['Invoice'] = _INVOICE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)

Invoice = _reflection.GeneratedProtocolMessageType('Invoice', (_message.Message,), dict(

  AccountBudgetSummary = _reflection.GeneratedProtocolMessageType('AccountBudgetSummary', (_message.Message,), dict(
    DESCRIPTOR = _INVOICE_ACCOUNTBUDGETSUMMARY,
    __module__ = 'google.ads.googleads_v4.proto.resources.invoice_pb2'
    ,
    __doc__ = """Represents a summarized account budget billable cost.
    
    
    Attributes:
        customer:
            Output only. The resource name of the customer associated with
            this account budget. This contains the customer ID, which
            appears on the invoice PDF as "Account ID". Customer resource
            names have the form:  ``customers/{customer_id}``
        customer_descriptive_name:
            Output only. The descriptive name of the account budget’s
            customer. It appears on the invoice PDF as "Account".
        account_budget:
            Output only. The resource name of the account budget
            associated with this summarized billable cost. AccountBudget
            resource names have the form:
            ``customers/{customer_id}/accountBudgets/{account_budget_id}``
        account_budget_name:
            Output only. The name of the account budget. It appears on the
            invoice PDF as "Account budget".
        purchase_order_number:
            Output only. The purchase order number of the account budget.
            It appears on the invoice PDF as "Purchase order".
        subtotal_amount_micros:
            Output only. The pretax subtotal amount attributable to this
            budget during the service period, in micros.
        tax_amount_micros:
            Output only. The tax amount attributable to this budget during
            the service period, in micros.
        total_amount_micros:
            Output only. The total amount attributable to this budget
            during the service period, in micros. This equals the sum of
            the account budget subtotal amount and the account budget tax
            amount.
        billable_activity_date_range:
            Output only. The billable activity date range of the account
            budget, within the service date range of this invoice. The end
            date is inclusive. This can be different from the account
            budget's start and end time.
    """,
    # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.resources.Invoice.AccountBudgetSummary)
    ))
  ,
  DESCRIPTOR = _INVOICE,
  __module__ = 'google.ads.googleads_v4.proto.resources.invoice_pb2'
  ,
  __doc__ = """An invoice. All invoice information is snapshotted to match the PDF
  invoice. For invoices older than the launch of InvoiceService, the
  snapshotted information may not match the PDF invoice.
  
  
  Attributes:
      resource_name:
          Output only. The resource name of the invoice. Multiple
          customers can share a given invoice, so multiple resource
          names may point to the same invoice. Invoice resource names
          have the form:
          ``customers/{customer_id}/invoices/{invoice_id}``
      id:
          Output only. The ID of the invoice. It appears on the invoice
          PDF as "Invoice number".
      type:
          Output only. The type of invoice.
      billing_setup:
          Output only. The resource name of this invoice’s billing
          setup.
          ``customers/{customer_id}/billingSetups/{billing_setup_id}``
      payments_account_id:
          Output only. A 16 digit ID used to identify the payments
          account associated with the billing setup, e.g.
          "1234-5678-9012-3456". It appears on the invoice PDF as
          "Billing Account Number".
      payments_profile_id:
          Output only. A 12 digit ID used to identify the payments
          profile associated with the billing setup, e.g.
          "1234-5678-9012". It appears on the invoice PDF as "Billing
          ID".
      issue_date:
          Output only. The issue date in yyyy-mm-dd format. It appears
          on the invoice PDF as either "Issue date" or "Invoice date".
      due_date:
          Output only. The due date in yyyy-mm-dd format.
      service_date_range:
          Output only. The service period date range of this invoice.
          The end date is inclusive.
      currency_code:
          Output only. The currency code. All costs are returned in this
          currency. A subset of the currency codes derived from the ISO
          4217 standard is supported.
      invoice_level_adjustments_micros:
          Output only. The total amount of invoice level adjustments.
          These adjustments are made on the invoice, not on a specific
          account budget.
      subtotal_amount_micros:
          Output only. The pretax subtotal amount, in micros. This
          equals the sum of the AccountBudgetSummary subtotal amounts,
          plus the invoice level adjustments.
      tax_amount_micros:
          Output only. The sum of all taxes on the invoice, in micros.
          This equals the sum of the AccountBudgetSummary tax amounts,
          plus taxes not associated with a specific account budget.
      total_amount_micros:
          Output only. The total amount, in micros. This equals the sum
          of the invoice subtotal amount and the invoice tax amount.
      corrected_invoice:
          Output only. The resource name of the original invoice
          corrected, wrote off, or canceled by this invoice, if
          applicable. If ``corrected_invoice`` is set,
          ``replaced_invoices`` will not be set. Invoice resource names
          have the form:
          ``customers/{customer_id}/invoices/{invoice_id}``
      replaced_invoices:
          Output only. The resource name of the original invoice(s)
          being rebilled or replaced by this invoice, if applicable.
          There might be multiple replaced invoices due to invoice
          consolidation. The replaced invoices may not belong to the
          same payments account. If ``replaced_invoices`` is set,
          ``corrected_invoice`` will not be set. Invoice resource names
          have the form:
          ``customers/{customer_id}/invoices/{invoice_id}``
      pdf_url:
          Output only. The URL to a PDF copy of the invoice. Users need
          to pass in their OAuth token to request the PDF with this URL.
      account_budget_summaries:
          Output only. The list of summarized account budget information
          associated with this invoice.
  """,
  # @@protoc_insertion_point(class_scope:google.ads.googleads.v4.resources.Invoice)
  ))
_sym_db.RegisterMessage(Invoice)
_sym_db.RegisterMessage(Invoice.AccountBudgetSummary)


DESCRIPTOR._options = None
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['customer']._options = None
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['customer_descriptive_name']._options = None
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['account_budget']._options = None
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['account_budget_name']._options = None
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['purchase_order_number']._options = None
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['subtotal_amount_micros']._options = None
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['tax_amount_micros']._options = None
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['total_amount_micros']._options = None
_INVOICE_ACCOUNTBUDGETSUMMARY.fields_by_name['billable_activity_date_range']._options = None
_INVOICE.fields_by_name['resource_name']._options = None
_INVOICE.fields_by_name['id']._options = None
_INVOICE.fields_by_name['type']._options = None
_INVOICE.fields_by_name['billing_setup']._options = None
_INVOICE.fields_by_name['payments_account_id']._options = None
_INVOICE.fields_by_name['payments_profile_id']._options = None
_INVOICE.fields_by_name['issue_date']._options = None
_INVOICE.fields_by_name['due_date']._options = None
_INVOICE.fields_by_name['service_date_range']._options = None
_INVOICE.fields_by_name['currency_code']._options = None
_INVOICE.fields_by_name['invoice_level_adjustments_micros']._options = None
_INVOICE.fields_by_name['subtotal_amount_micros']._options = None
_INVOICE.fields_by_name['tax_amount_micros']._options = None
_INVOICE.fields_by_name['total_amount_micros']._options = None
_INVOICE.fields_by_name['corrected_invoice']._options = None
_INVOICE.fields_by_name['replaced_invoices']._options = None
_INVOICE.fields_by_name['pdf_url']._options = None
_INVOICE.fields_by_name['account_budget_summaries']._options = None
_INVOICE._options = None
# @@protoc_insertion_point(module_scope)
