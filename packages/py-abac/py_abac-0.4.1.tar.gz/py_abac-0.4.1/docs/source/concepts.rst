.. _concepts:

Concepts
########

`ABAC <https://en.wikipedia.org/wiki/Attribute-based_access_control>`_ gives you a fine-grained control on definition
of the rules that restrict access to resources and is generally considered a "next generation" authorization model. In
the following section we describe the different components of ABAC.

.. _abac_arch:

Access Control Architecture
===========================


.. image:: https://lh6.googleusercontent.com/z4oppCjtEITgem5UZUN28NiaV4LrYPrjqD1MjZiYDhjmj1OkFFcN9H2jj64Zd0tkRkf5O436eOA574Sur0uSDlUztRtadREn_wfRfMbh4dNiACxivd0zjM_gLcF94N-bdhl_g15N
   :target: https://lh6.googleusercontent.com/z4oppCjtEITgem5UZUN28NiaV4LrYPrjqD1MjZiYDhjmj1OkFFcN9H2jj64Zd0tkRkf5O436eOA574Sur0uSDlUztRtadREn_wfRfMbh4dNiACxivd0zjM_gLcF94N-bdhl_g15N
   :alt: img


The above diagram depicts the standard architecture for ABAC, which is as follows:

.. _abac_pep:

- **The PEP or Policy Enforcement Point**:
  It is your piece of code that uses py-ABAC to protect  app & data. The PEP should  inspect a user request, create a
  corresponding access request, and send it to the PDP for evaluation.

.. _abac_pdp:

- **The PDP or Policy Decision Point**:
  It is the brain of the architecture. This is the piece which evaluates incoming access requests against policies and
  returns a Permit / Deny decision. The PDP may also use PIPs to retrieve missing attribute values during policy evaluation.

.. _abac_pip:

- **The PIP or Policy Information Point**:
  This bridges the PDP to external sources of attribute values e.g. LDAP or databases.

.. _abac_pap:

- **The PAP or Policy Administration Point**:
  This manages the creation, update and deletion of policies evaluated by PDP.


Access Control Elements
=======================

In the above architecture, following four elements are involved during an access request to PDP:


- **subject**\ : This is the entity which requests access, also known as the request principal. A subject can be anything that requests access, i.e. a user or an application.
- **resource**\ : The object which is requested to be accessed by the subject.
- **action**\ : The action being performed on the resource.
- **context**\ : This element deals with time, location or dynamic aspects of the access control scenario.

In py-ABAC one defines policies containing conditions on one or more attributes of these four elements. If these conditions are satisfied, an access decision is returned by the PDP using an evaluation algorithm. There are three different evaluation algorithms supported:

.. _allow_overrides:

#. :class:`AllowOverrides`: returns :code:`allow` if any decision evaluates to :code:`allow`; and returns :code:`deny` if all decisions evaluate to :code:`deny`.

.. _deny_overrides:

#. :class:`DenyOverrides`: returns :code:`deny` if any decision evaluates to :code:`deny`; returns :code:`allow` if all decisions evaluate to :code:`allow`.

.. _highest_priority:

#. :class:`HighestPriority`: returns the highest priority decision that evaluates to either :code:`allow` or :code:`deny`. If there are multiple equally highest priority decisions that conflict, then :class:`DenyOverrides` algorithm would be applied among those highest priority decisions.
