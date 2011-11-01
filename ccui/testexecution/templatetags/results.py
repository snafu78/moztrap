# Case Conductor is a Test Case Management system.
# Copyright (C) 2011 uTest Inc.
# 
# This file is part of Case Conductor.
# 
# Case Conductor is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Case Conductor is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Case Conductor.  If not, see <http://www.gnu.org/licenses/>.
from django import template
from django.core.urlresolvers import reverse

from ..models import TestCycle, TestRun, TestRunIncludedTestCase



register = template.Library()



@register.filter
def results_detail_url(obj):
    if isinstance(obj, TestCycle):
        return reverse("results_testruns") + "?testCycle=%s" % obj.id
    elif isinstance(obj, TestRun):
        return reverse("results_testcases") + "?testRun=%s" % obj.id
    elif isinstance(obj, TestRunIncludedTestCase):
        return reverse("results_testcase_detail", kwargs={"itc_id": obj.id})
    return ""
