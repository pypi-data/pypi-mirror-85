
def query(q):
    """
    Perform a raw query.

    Args:
        q (str): The query to run

    Example:
        >>> import mage
        >>> mage.connect()
        >>> mage.query("listAssessments { items {id}, nextToken }")
    """

    from mage import endpoint
    q = 'query {%s}' % q
    return endpoint(query=q)

def mutate(q):
    """
    Perform a raw mutation.

    Args:
        q (str): The mutation to run

    Example:
        >>> import mage
        >>> mage.connect()
        >>> mage.mutate("createAssessment(input: {type: EXTERNAL, name: "test", assessmentClientId: "12345"}) {id})
    """
    from mage import endpoint
    q = 'mutation {%s}' % q
    return endpoint(query=q)
