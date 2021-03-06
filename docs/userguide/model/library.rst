Test Cases and Suites
=====================

.. _test-cases:

Test Cases
----------

A **Test Case** is a named set of steps for testing a single feature or
characteristic of the system under test. Test cases are associated with a
:ref:`product <products>`, and can have one version per :ref:`product
version<product-versions>`. They can be organized via :ref:`suites
<test-suites>` and/or :ref:`tags<tags>`, and can have file
:ref:`attachments<attachments>`. Preconditions, assumptions, and other
preliminary information can be provided in the case's *description*. A test
case can have any number of steps; each step has an *instruction* and an
*expected result*.

.. _test-case-edit-fields:

Case Edit Fields
^^^^^^^^^^^^^^^^

* **Product** - The product that owns this test case.
* **Version** - The product version of this test case.
* **And Later Versions** - Create a test case version for the specified Product
  Version as well as a case version for each later Product Version.  (e.g.: if
  Product Versions 3, 4 and 5 exist for this Product, and you have specified
  Product Version 4, this case will be created for versions 4 and 5)
* **Suite** - (optional) The existing suite to which you want this case to
  belong.
  You can also add cases to suites later.
* **Name** - The summary name for the case.
* **Description** - Any description, pre-conditions, links or notes to
  associate with the case.  This field is displayed while running the test.
  Markdown syntax is supported.
* **Add Tags** - Enter tags to apply to this case.  Hit enter after each tag to
  see the tag chicklet displayed.  Auto-completes for existing tags.
* **Add Attachment** - You can attach files to cases that may help running the
  test.  (e.g: images, audio, video, etc.)
* **Instruction / Expected** - The test instruction and corresponding expected
  result.  You can choose to put all instructions / expectations in one step,
  or break them down to individual steps.  When running the test, you will have
  the option to fail on specific steps, so you may find this a better approach.
  Markdown syntax is supported.
* **Save** - You can choose to save the case as draft or active.  Only active
  cases can be run in a test run.

.. _test-suites:

Test Suites
-----------

A **Test Suite** is a named collection of test cases that can be included in a
:ref:`test run<test-runs>`.

.. _test-suite-edit-fields:

Suite Edit Fields
^^^^^^^^^^^^^^^^^

* **Product** - The product that owns this test case.
* **Name** - The name of the suite.
* **Description** - Any description for the suite.
* **Available Cases** - Test Cases that have the same Product you selected for this
  suite.  This list is filterable.
* **Included Cases** - Test Cases that are included in the Suite.  This list is not
  filtered.

.. _tags:

Tags
----

A **Tag** can be associated with one or more :ref:`test cases<test-cases>` as a
way to organize and filter them on any number of axes.

By default, tags are :ref:`product<products>`-specific; global tags can also be
created and managed via the tag management UI.

.. _tag-edit-fields:

Tag Edit Fields
^^^^^^^^^^^^^^^

* **Name** - The name of the tag.
* **Product** - (optional) Tags can be specific to a Product, or they can be
  global.  If a tag is Product specific, then cases for other products can't
  use it.  This is useful if you want to separate tags for different products.


.. _attachments:

Attachments
-----------

A :ref:`test case<test-cases>` can have any number of file attachments: these
will be made available for download by testers when the test case is executed.
