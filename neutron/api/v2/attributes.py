# Copyright (c) 2012 OpenStack Foundation.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

from neutron_lib.api import converters as lib_converters
from neutron_lib.api import validators as lib_validators
from neutron_lib import constants
import six
import webob.exc

from neutron._i18n import _


# Defining a constant to avoid repeating string literal in several modules
SHARED = 'shared'

# TODO(HenryG): use DB field sizes (neutron-lib 0.1.1)
NAME_MAX_LEN = 255
TENANT_ID_MAX_LEN = 255
DESCRIPTION_MAX_LEN = 255
LONG_DESCRIPTION_MAX_LEN = 1024
DEVICE_ID_MAX_LEN = 255
DEVICE_OWNER_MAX_LEN = 255

# Define constants for base resource name
NETWORK = 'network'
NETWORKS = '%ss' % NETWORK
PORT = 'port'
PORTS = '%ss' % PORT
SUBNET = 'subnet'
SUBNETS = '%ss' % SUBNET
SUBNETPOOL = 'subnetpool'
SUBNETPOOLS = '%ss' % SUBNETPOOL
# Note: a default of ATTR_NOT_SPECIFIED indicates that an
# attribute is not required, but will be generated by the plugin
# if it is not specified.  Particularly, a value of ATTR_NOT_SPECIFIED
# is different from an attribute that has been specified with a value of
# None.  For example, if 'gateway_ip' is omitted in a request to
# create a subnet, the plugin will receive ATTR_NOT_SPECIFIED
# and the default gateway_ip will be generated.
# However, if gateway_ip is specified as None, this means that
# the subnet does not have a gateway IP.
# The following is a short reference for understanding attribute info:
# default: default value of the attribute (if missing, the attribute
# becomes mandatory.
# allow_post: the attribute can be used on POST requests.
# allow_put: the attribute can be used on PUT requests.
# validate: specifies rules for validating data in the attribute.
# convert_to: transformation to apply to the value before it is returned
# is_visible: the attribute is returned in GET responses.
# required_by_policy: the attribute is required by the policy engine and
# should therefore be filled by the API layer even if not present in
# request body.
# enforce_policy: the attribute is actively part of the policy enforcing
# mechanism, ie: there might be rules which refer to this attribute.

RESOURCE_ATTRIBUTE_MAP = {
    NETWORKS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True,
                 'validate': {'type:string': NAME_MAX_LEN},
                 'default': '', 'is_visible': True},
        'subnets': {'allow_post': False, 'allow_put': False,
                    'default': [],
                    'is_visible': True},
        'admin_state_up': {'allow_post': True, 'allow_put': True,
                           'default': True,
                           'convert_to': lib_converters.convert_to_boolean,
                           'is_visible': True},
        'status': {'allow_post': False, 'allow_put': False,
                   'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:string': TENANT_ID_MAX_LEN},
                      'required_by_policy': True,
                      'is_visible': True},
        SHARED: {'allow_post': True,
                 'allow_put': True,
                 'default': False,
                 'convert_to': lib_converters.convert_to_boolean,
                 'is_visible': True,
                 'required_by_policy': True,
                 'enforce_policy': True},
    },
    PORTS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True, 'default': '',
                 'validate': {'type:string': NAME_MAX_LEN},
                 'is_visible': True},
        'network_id': {'allow_post': True, 'allow_put': False,
                       'required_by_policy': True,
                       'validate': {'type:uuid': None},
                       'is_visible': True},
        'admin_state_up': {'allow_post': True, 'allow_put': True,
                           'default': True,
                           'convert_to': lib_converters.convert_to_boolean,
                           'is_visible': True},
        'mac_address': {'allow_post': True, 'allow_put': True,
                        'default': constants.ATTR_NOT_SPECIFIED,
                        'validate': {'type:mac_address': None},
                        'enforce_policy': True,
                        'is_visible': True},
        'fixed_ips': {'allow_post': True, 'allow_put': True,
                      'default': constants.ATTR_NOT_SPECIFIED,
                      'convert_list_to':
                          lib_converters.convert_kvp_list_to_dict,
                      'validate': {'type:fixed_ips': None},
                      'enforce_policy': True,
                      'is_visible': True},
        'device_id': {'allow_post': True, 'allow_put': True,
                      'validate': {'type:string': DEVICE_ID_MAX_LEN},
                      'default': '',
                      'is_visible': True},
        'device_owner': {'allow_post': True, 'allow_put': True,
                         'validate': {'type:string': DEVICE_OWNER_MAX_LEN},
                         'default': '', 'enforce_policy': True,
                         'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:string': TENANT_ID_MAX_LEN},
                      'required_by_policy': True,
                      'is_visible': True},
        'status': {'allow_post': False, 'allow_put': False,
                   'is_visible': True},
    },
    SUBNETS: {
        'id': {'allow_post': False, 'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True},
        'name': {'allow_post': True, 'allow_put': True, 'default': '',
                 'validate': {'type:string': NAME_MAX_LEN},
                 'is_visible': True},
        'ip_version': {'allow_post': True, 'allow_put': False,
                       'convert_to': lib_converters.convert_to_int,
                       'validate': {'type:values': [4, 6]},
                       'is_visible': True},
        'network_id': {'allow_post': True, 'allow_put': False,
                       'required_by_policy': True,
                       'validate': {'type:uuid': None},
                       'is_visible': True},
        'subnetpool_id': {'allow_post': True,
                          'allow_put': False,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'required_by_policy': False,
                          'validate': {'type:subnetpool_id_or_none': None},
                          'is_visible': True},
        'prefixlen': {'allow_post': True,
                      'allow_put': False,
                      'validate': {'type:non_negative': None},
                      'convert_to': lib_converters.convert_to_int,
                      'default': constants.ATTR_NOT_SPECIFIED,
                      'required_by_policy': False,
                      'is_visible': False},
        'cidr': {'allow_post': True,
                 'allow_put': False,
                 'default': constants.ATTR_NOT_SPECIFIED,
                 'validate': {'type:subnet_or_none': None},
                 'required_by_policy': False,
                 'is_visible': True},
        'gateway_ip': {'allow_post': True, 'allow_put': True,
                       'default': constants.ATTR_NOT_SPECIFIED,
                       'validate': {'type:ip_address_or_none': None},
                       'is_visible': True},
        'allocation_pools': {'allow_post': True, 'allow_put': True,
                             'default': constants.ATTR_NOT_SPECIFIED,
                             'validate': {'type:ip_pools': None},
                             'is_visible': True},
        'dns_nameservers': {'allow_post': True, 'allow_put': True,
                            'convert_to':
                                lib_converters.convert_none_to_empty_list,
                            'default': constants.ATTR_NOT_SPECIFIED,
                            'validate': {'type:nameservers': None},
                            'is_visible': True},
        'host_routes': {'allow_post': True, 'allow_put': True,
                        'convert_to':
                            lib_converters.convert_none_to_empty_list,
                        'default': constants.ATTR_NOT_SPECIFIED,
                        'validate': {'type:hostroutes': None},
                        'is_visible': True},
        'tenant_id': {'allow_post': True, 'allow_put': False,
                      'validate': {'type:string': TENANT_ID_MAX_LEN},
                      'required_by_policy': True,
                      'is_visible': True},
        'enable_dhcp': {'allow_post': True, 'allow_put': True,
                        'default': True,
                        'convert_to': lib_converters.convert_to_boolean,
                        'is_visible': True},
        'ipv6_ra_mode': {'allow_post': True, 'allow_put': False,
                         'default': constants.ATTR_NOT_SPECIFIED,
                         'validate': {'type:values': constants.IPV6_MODES},
                         'is_visible': True},
        'ipv6_address_mode': {'allow_post': True, 'allow_put': False,
                              'default': constants.ATTR_NOT_SPECIFIED,
                              'validate': {'type:values':
                                           constants.IPV6_MODES},
                              'is_visible': True},
        SHARED: {'allow_post': False,
                 'allow_put': False,
                 'default': False,
                 'convert_to': lib_converters.convert_to_boolean,
                 'is_visible': False,
                 'required_by_policy': True,
                 'enforce_policy': True},
    },
    SUBNETPOOLS: {
        'id': {'allow_post': False,
               'allow_put': False,
               'validate': {'type:uuid': None},
               'is_visible': True,
               'primary_key': True},
        'name': {'allow_post': True,
                 'allow_put': True,
                 'validate': {'type:not_empty_string': None},
                 'is_visible': True},
        'tenant_id': {'allow_post': True,
                      'allow_put': False,
                      'validate': {'type:string': TENANT_ID_MAX_LEN},
                      'required_by_policy': True,
                      'is_visible': True},
        'prefixes': {'allow_post': True,
                     'allow_put': True,
                     'validate': {'type:subnet_list': None},
                     'is_visible': True},
        'default_quota': {'allow_post': True,
                          'allow_put': True,
                          'validate': {'type:non_negative': None},
                          'convert_to': lib_converters.convert_to_int,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'is_visible': True},
        'ip_version': {'allow_post': False,
                       'allow_put': False,
                       'is_visible': True},
        'default_prefixlen': {'allow_post': True,
                              'allow_put': True,
                              'validate': {'type:non_negative': None},
                              'convert_to': lib_converters.convert_to_int,
                              'default': constants.ATTR_NOT_SPECIFIED,
                              'is_visible': True},
        'min_prefixlen': {'allow_post': True,
                          'allow_put': True,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'validate': {'type:non_negative': None},
                          'convert_to': lib_converters.convert_to_int,
                          'is_visible': True},
        'max_prefixlen': {'allow_post': True,
                          'allow_put': True,
                          'default': constants.ATTR_NOT_SPECIFIED,
                          'validate': {'type:non_negative': None},
                          'convert_to': lib_converters.convert_to_int,
                          'is_visible': True},
        'is_default': {'allow_post': True,
                       'allow_put': True,
                       'default': False,
                       'convert_to': lib_converters.convert_to_boolean,
                       'is_visible': True,
                       'required_by_policy': True,
                       'enforce_policy': True},
        SHARED: {'allow_post': True,
                 'allow_put': False,
                 'default': False,
                 'convert_to': lib_converters.convert_to_boolean,
                 'is_visible': True,
                 'required_by_policy': True,
                 'enforce_policy': True},
    }
}

# Identify the attribute used by a resource to reference another resource

RESOURCE_FOREIGN_KEYS = {
    NETWORKS: 'network_id'
}

# Store plural/singular mappings
PLURALS = {NETWORKS: NETWORK,
           PORTS: PORT,
           SUBNETS: SUBNET,
           SUBNETPOOLS: SUBNETPOOL,
           'dns_nameservers': 'dns_nameserver',
           'host_routes': 'host_route',
           'allocation_pools': 'allocation_pool',
           'fixed_ips': 'fixed_ip',
           'extensions': 'extension'}
# Store singular/plural mappings. This dictionary is populated by
# get_resource_info
REVERSED_PLURALS = {}


def get_collection_info(collection):
    """Helper function to retrieve attribute info.

    :param collection: Collection or plural name of the resource
    """
    return RESOURCE_ATTRIBUTE_MAP.get(collection)


def get_resource_info(resource):
    """Helper function to retrieve attribute info

    :param resource: resource name
    """
    plural_name = REVERSED_PLURALS.get(resource)
    if not plural_name:
        for (plural, singular) in PLURALS.items():
            if singular == resource:
                plural_name = plural
                REVERSED_PLURALS[resource] = plural_name
    return RESOURCE_ATTRIBUTE_MAP.get(plural_name)


def fill_default_value(attr_info, res_dict,
                       exc_cls=ValueError,
                       check_allow_post=True):
    for attr, attr_vals in six.iteritems(attr_info):
        if attr_vals['allow_post']:
            if 'default' not in attr_vals and attr not in res_dict:
                msg = _("Failed to parse request. Required "
                        "attribute '%s' not specified") % attr
                raise exc_cls(msg)
            res_dict[attr] = res_dict.get(attr,
                                          attr_vals.get('default'))
        elif check_allow_post:
            if attr in res_dict:
                msg = _("Attribute '%s' not allowed in POST") % attr
                raise exc_cls(msg)


def convert_value(attr_info, res_dict, exc_cls=ValueError):
    for attr, attr_vals in six.iteritems(attr_info):
        if (attr not in res_dict or
                res_dict[attr] is constants.ATTR_NOT_SPECIFIED):
            continue
        # Convert values if necessary
        if 'convert_to' in attr_vals:
            res_dict[attr] = attr_vals['convert_to'](res_dict[attr])
        # Check that configured values are correct
        if 'validate' not in attr_vals:
            continue
        for rule in attr_vals['validate']:
            validator = lib_validators.get_validator(rule)
            res = validator(res_dict[attr], attr_vals['validate'][rule])

            if res:
                msg_dict = dict(attr=attr, reason=res)
                msg = _("Invalid input for %(attr)s. "
                        "Reason: %(reason)s.") % msg_dict
                raise exc_cls(msg)


def populate_project_info(attributes):
    """
    Ensure that both project_id and tenant_id attributes are present.

    If either project_id or tenant_id is present in attributes then ensure
    that both are present.

    If neither are present then attributes is not updated.

    :param attributes: a dictionary of resource/API attributes
    :type attributes: dict

    :return: the updated attributes dictionary
    :rtype: dict
    """
    if 'tenant_id' in attributes and 'project_id' not in attributes:
        # TODO(HenryG): emit a deprecation warning here
        attributes['project_id'] = attributes['tenant_id']
    elif 'project_id' in attributes and 'tenant_id' not in attributes:
        # Backward compatibility for code still using tenant_id
        attributes['tenant_id'] = attributes['project_id']

    if attributes.get('project_id') != attributes.get('tenant_id'):
        msg = _("'project_id' and 'tenant_id' do not match")
        raise webob.exc.HTTPBadRequest(msg)

    return attributes


def _validate_privileges(context, res_dict):
    if ('project_id' in res_dict and
            res_dict['project_id'] != context.project_id and
            not context.is_admin):
        msg = _("Specifying 'project_id' or 'tenant_id' other than "
                "authenticated project in request requires admin privileges")
        raise webob.exc.HTTPBadRequest(msg)


def populate_tenant_id(context, res_dict, attr_info, is_create):
    populate_project_info(res_dict)
    _validate_privileges(context, res_dict)

    if is_create and 'project_id' not in res_dict:
        if context.project_id:
            res_dict['project_id'] = context.project_id

            # For backward compatibility
            res_dict['tenant_id'] = context.project_id

        elif 'tenant_id' in attr_info:
            msg = _("Running without keystone AuthN requires "
                    "that tenant_id is specified")
            raise webob.exc.HTTPBadRequest(msg)


def verify_attributes(res_dict, attr_info):
    populate_project_info(attr_info)

    extra_keys = set(res_dict.keys()) - set(attr_info.keys())
    if extra_keys:
        msg = _("Unrecognized attribute(s) '%s'") % ', '.join(extra_keys)
        raise webob.exc.HTTPBadRequest(msg)
