#!/usr/bin/env python

# author Huy 
# date 9/23/2019

from api.base_const import const


class Workday(const):
    MORNING = 'Morning'
    AFTERNOON = 'Afternoon'
    FULL = 'Full day'

    TYPES = (
        (MORNING, 'Morning'),
        (AFTERNOON, 'Afternoon'),
        (FULL, 'Full day')
    )

    LEAVE = 'Leave'
    REMOTE = 'Remote work'

    DEFAULT_START_HOUR = '08:00'
    DEFAULT_END_HOUR = '17:30'

    STATUS_ACCEPTED = 'Accepted'
    STATUS_PASSED = 'Passed'
    STATUS_PENDING = 'Pending'
    STATUS_REJECTED = 'Rejected'
