def test_serialize():
    from pypom_form.fields import ObjectType

    assert ObjectType.serialize(None, [1, 2, 3]) == [1, 2, 3]


def test_deserialize():
    from pypom_form.fields import ObjectType

    assert ObjectType.deserialize(None, [1, 2, 3]) == [1, 2, 3]
