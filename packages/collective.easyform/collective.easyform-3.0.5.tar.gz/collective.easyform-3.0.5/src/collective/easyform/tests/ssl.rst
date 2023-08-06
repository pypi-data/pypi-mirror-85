'Force SSL' setting
-------------------

First let's get our test browser and make sure that it won't re-raise Redirect errors::

    >>> browser = get_browser(layer)
    >>> from ZPublisher import HTTPResponse
    >>> HTTPResponse.status_codes['movedtemporarily'] = 200

Set up a form with the 'force SSL' setting on::

    >>> portal_url = layer['portal'].absolute_url()
    >>> browser.open(portal_url)
    >>> browser.getLink('EasyForm').click()
    >>> browser.getControl('Title').value = 'testform'
    >>> browser.getControl('Force SSL connection').selected = True
    >>> browser.getControl('Save').click()
    >>> 'Item created' in browser.contents
    True
    >>> browser.url
    '.../testform/...'
    >>> 'Location' in browser.headers
    False

Note that we didn't get forced to SSL immediately after creating the form.  (Which
would have raised a testbrowser error.)  That's because for people who have permission
to edit the form, 'force SSL' only takes place *on form submission*.

However, the form action should be set to an https URL so that the submission will still
be secure::

    >>> 'action="https://' in browser.contents
    True

Finally, let's use a new browser that isn't authenticated, and confirm that for someone
who doesn't have permission to edit the form, SSL will be forced on initial form load as
well (so the user sees a security icon in their browser.) ::

    >>> browser.open(portal_url + '/testform/content_status_modify?workflow_action=publish')
    >>> 'Item state changed' in browser.contents
    True

Log out and go back to the form.
We should be redirected to https://
::

    >>> anon_browser = get_browser(layer, auth=False)
    >>> anon_browser.open(portal_url + '/testform')
    >>> 'Location' in anon_browser.headers
    True
    >>> anon_browser.headers['Location']
    'https://nohost/plone/testform/view'

