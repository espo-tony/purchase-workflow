==============================================
Purchase Work Acceptance - Late Delivery Fines
==============================================

.. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Alpha-red.png
    :target: https://odoo-community.org/page/development-status
    :alt: Alpha
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fpurchase--workflow-lightgray.png?logo=github
    :target: https://github.com/OCA/purchase-workflow/tree/15.0/purchase_work_acceptance_late_fines
    :alt: OCA/purchase-workflow
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/purchase-workflow-15-0/purchase-workflow-15-0-purchase_work_acceptance_late_fines
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runbot-Try%20me-875A7B.png
    :target: https://runbot.odoo-community.org/runbot/142/15.0
    :alt: Try me on Runbot

|badge1| |badge2| |badge3| |badge4| |badge5| 

This module extends Purchase Work Acceptance by adding the ability to calculate late delivery fines to vendor.

.. IMPORTANT::
   This is an alpha version, the data model and design can change at any time without warning.
   Only for development or testing purpose, do not use in production.
   `More details on development status <https://odoo-community.org/page/development-status>`_

**Table of contents**

.. contents::
   :local:

Configuration
=============

** Show Fines Tab on Work Acceptance **

#. Go to *Purchase > Configuration > Settings*
#. Check 'Enable Late Delivery Fines on Work Acceptance'
#. Add the account and default fines rate (per day)

Usage
=====

**Usual process of Purchasing with Work Acceptance**

#. Create a Purchase Order > Work Acceptance
#. Set Due Date on Work Acceptance
#. It will calculate Late Days and Fines Amount automatic (adjustable)
#. Accept the Work Acceptance
#. Generate Fines Invoice by clicking "Create Fines Invoice" button, which includes the configured default account code.
#. Normally process

**Create Fines from Work Acceptance**

#. Go to Purchase > Orders > Work Acceptance
#. In List View, Select all you have to create fines invoice > Action > Create Fines Invoice
#. In Form View, Select work acceptance > click `Create Fines Invoice` button

**Create Fines from Invoice**

#. Go to Invoicing > Customers > Invoices > Create
#. Select Late WA (wa is delivery late)
#. It will automatically generate lines.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/purchase-workflow/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/OCA/purchase-workflow/issues/new?body=module:%20purchase_work_acceptance_late_fines%0Aversion:%2015.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Ecosoft

Contributors
~~~~~~~~~~~~

* `Ecosoft <http://ecosoft.co.th>`__:

  * Saran Lim. <saranl@ecosoft.co.th>
  * Kitti U. <kittiu@ecosoft.co.th>

* `ProThai <http://prothaitechnology.com>`__:

  * Prapassorn Sornkaew <prapassorn.s@prothaitechnology.com>

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-Saran440| image:: https://github.com/Saran440.png?size=40px
    :target: https://github.com/Saran440
    :alt: Saran440

Current `maintainer <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-Saran440| 

This module is part of the `OCA/purchase-workflow <https://github.com/OCA/purchase-workflow/tree/15.0/purchase_work_acceptance_late_fines>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
