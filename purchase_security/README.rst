=======================
Purchase Order security
=======================

.. !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
   !! This file is generated by oca-gen-addon-readme !!
   !! changes will be overwritten.                   !!
   !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

.. |badge1| image:: https://img.shields.io/badge/maturity-Production%2FStable-green.png
    :target: https://odoo-community.org/page/development-status
    :alt: Production/Stable
.. |badge2| image:: https://img.shields.io/badge/licence-AGPL--3-blue.png
    :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
    :alt: License: AGPL-3
.. |badge3| image:: https://img.shields.io/badge/github-OCA%2Fpurchase--workflow-lightgray.png?logo=github
    :target: https://github.com/OCA/purchase-workflow/tree/15.0/purchase_security
    :alt: OCA/purchase-workflow
.. |badge4| image:: https://img.shields.io/badge/weblate-Translate%20me-F47D42.png
    :target: https://translation.odoo-community.org/projects/purchase-workflow-15-0/purchase-workflow-15-0-purchase_security
    :alt: Translate me on Weblate
.. |badge5| image:: https://img.shields.io/badge/runbot-Try%20me-875A7B.png
    :target: https://runbot.odoo-community.org/runbot/142/15.0
    :alt: Try me on Runbot

|badge1| |badge2| |badge3| |badge4| |badge5| 

This addon creates a new group called "Purchase (own orders)" in Purchase.

For users in this group, the only Purchase Orders they can see are those where
they are the representative, or all of them if they are managers.

**Table of contents**

.. contents::
   :local:

Usage
=====

To use this module, you need to:

#. Go to **Purchase > Orders > Purchase Orders**
#. Create a Purchase Order and assing a **Purchase Representative**
   (in the **Other Information** tab). By default, it will be the current user.
#. Confirm the Purchase Order
#. Go back to the **Purchase Orders** view.
#. If you are the Purchase Representative or a Purchase Manager, you should be
   able to see the order you created. If not, you shouldn't.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/OCA/purchase-workflow/issues>`_.
In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smashing it by providing a detailed and welcomed
`feedback <https://github.com/OCA/purchase-workflow/issues/new?body=module:%20purchase_security%0Aversion:%2015.0%0A%0A**Steps%20to%20reproduce**%0A-%20...%0A%0A**Current%20behavior**%0A%0A**Expected%20behavior**>`_.

Do not contact contributors directly about support or help with technical issues.

Credits
=======

Authors
~~~~~~~

* Tecnativa

Contributors
~~~~~~~~~~~~

* `Tecnativa <https://www.tecnativa.com>`_:

  * João Marques
  * Pilar Vargas

Maintainers
~~~~~~~~~~~

This module is maintained by the OCA.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

.. |maintainer-pilarvargas-tecnativa| image:: https://github.com/pilarvargas-tecnativa.png?size=40px
    :target: https://github.com/pilarvargas-tecnativa
    :alt: pilarvargas-tecnativa

Current `maintainer <https://odoo-community.org/page/maintainer-role>`__:

|maintainer-pilarvargas-tecnativa| 

This module is part of the `OCA/purchase-workflow <https://github.com/OCA/purchase-workflow/tree/15.0/purchase_security>`_ project on GitHub.

You are welcome to contribute. To learn how please visit https://odoo-community.org/page/Contribute.
