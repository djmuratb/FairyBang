# -*- coding: utf-8 -*-
import re


# Change value from inline markup.
PN_SET              = re.compile(r'SET:(?P<value>.+)')
# Change value from reply markup (steps processes).
PN_ENTER            = re.compile(r'ENTER:(?P<value>.+)')

# Updates value of specific catalog setting.
PN_CAT_SET          = re.compile(r'SET:(?P<setting_name>.+)')
# Displays girls profiles.
PN_CAT              = re.compile(r'CAT:(?P<profiles_limit>\d{1,2})')
# Shows more girls profiles.
PN_CAT_MORE         = re.compile(r'MORE:(?P<profiles_limit>\d{1,2})')
# Girl profile details.
PN_CAT_PROFILE      = re.compile(r'PROFILE:(?P<profile_id>\d+)')
# Returns back from detail girls profile to base girl info.
PN_CAT_BACK         = re.compile(r'BACK:(?P<profile_id>\d+)')
# Girl profile payment.
PN_CAT_PAY          = re.compile(r'PAY:(?P<profile_id>\d+)')

# Displays available options of specific filters.
PN_FIL              = re.compile(r'^FIL:(?P<filter_name>.+)$')
# Changing filter option.
PN_FIL_OP           = re.compile(r'^OP:(?P<filter_name>.+):(?P<option_name>.+)$')
# Moves to previous or next page of filter option.
PN_FIL_MOVE         = re.compile(r'MOVE:(?P<filter_name>.+):(prev|next)')
#
PN_FIL_ENTER        = re.compile(r'ENTER:(?P<value>.+)')

# Returns back from `changing enum option` message to last view filter options.
PN_CH_BACK          = re.compile(r'CH_BACK:(?P<filter_name>.+)')
# Displays message of changing enum option.
PN_CH_SET           = re.compile(r'CH:(?P<filter_name>.+):(?P<option_key>\w+):(?P<option_value>.+)')
