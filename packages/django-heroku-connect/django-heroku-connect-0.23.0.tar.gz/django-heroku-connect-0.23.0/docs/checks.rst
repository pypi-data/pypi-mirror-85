Checks
======

Model Checks
------------

``heroku_connect.E001``
~~~~~~~~~~~~~~~~~~~~~~~

The class attribute :attr:`HerokuConnectModel.sf_object_name<heroku_connect.models.HerokuConnectModel.sf_object_name>` has not been set.

``heroku_connect.E002``
~~~~~~~~~~~~~~~~~~~~~~~

:attr:`HerokuConnectModel.sf_access<heroku_connect.models.HerokuConnectModel.sf_access>` must be either ``read_only`` or ``read_write``.

``heroku_connect.E003``
~~~~~~~~~~~~~~~~~~~~~~~

The model has fields with duplicate :attr:`HerokuConnectFieldMixin.sf_field_name<heroku_connect.models.HerokuConnectFieldMixin.sf_field_name>`.

``heroku_connect.E004``
~~~~~~~~~~~~~~~~~~~~~~~

More than one field is defined as :attr:`HerokuConnectFieldMixin.upsert<heroku_connect.models.HerokuConnectFieldMixin.upsert>`.

``heroku_connect.E005``
~~~~~~~~~~~~~~~~~~~~~~~

A related field (:class:`ForeignKey<django.db.models.ForeignKey>` or
:class:`ManyToManyField<django.db.models.ManyToManyField>`) points to the ``id``
field of a Heroku Connect model.

Heroku Connect uses the ``id`` column for internal purposes and may change it at any given time.
The ``id`` column should not be referenced, since it does not represent
a key for the Salesforce record. It is recommended to use an External ID or
the Salesforce ID ``sfid``.

.. note::
    Always use an External ID, if you want to write to Heroku Connect,
    see: https://devcenter.heroku.com/articles/writing-data-to-salesforce-with-heroku-connect#simple-relationships-between-two-objects-and-relationship-external-ids

``heroku_connect.E006``
~~~~~~~~~~~~~~~~~~~~~~~

The Salesforce object name must be unique since an object can only mapped to a
PostgreSQL table once.


``heroku_connect.E007``
~~~~~~~~~~~~~~~~~~~~~~~

Read-write mappings in Heroku Connect need to provide an upsert field to
identify the record.

``heroku_connect.E008``
~~~~~~~~~~~~~~~~~~~~~~~

A related field (:class:`ForeignKey<django.db.models.ForeignKey>` or
:class:`ManyToManyField<django.db.models.ManyToManyField>`) pointing to
a Heroku Connect model may not use database-constraints.

(previously ``heroku_connect.W001``)

.. note::
    Sometimes Heroku Connect needs to recreate the table, which breaks when
    if there are database constraints pointing to them.

    see: https://devcenter.heroku.com/articles/heroku-connect-logs-errors#error-during-sync-psycopg2-integrityerror-update-or-delete-on-table-mycustomobject__c-violates-foreign-key-constraint

``heroku_connect.W001``
~~~~~~~~~~~~~~~~~~~~~~~

Deprecated, changed to ``heroku_connect.E008``.

There are situations where Heroku Connect sync breaks if there is a database constraint
pointing to a Heroku-Connect table.
