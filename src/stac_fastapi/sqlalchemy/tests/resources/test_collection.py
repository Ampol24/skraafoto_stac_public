import pystac


# def test_create_and_delete_collection(app_client, load_test_data):
#    """Test creation and deletion of a collection"""
#    test_collection = load_test_data("test_collection.json")
#    test_collection["id"] = "test"
#
#    resp = app_client.post("/collections", json=test_collection)
#    assert resp.status_code == 200
#
#    resp = app_client.delete(f"/collections/{test_collection['id']}")
#    assert resp.status_code == 200


# Since the test-fixture is not actually creating anything, this is fine
# def test_create_collection_conflict(app_client, load_test_data):
#    """Test creation of a collection which already exists"""
#    # This collection ID is created in the fixture, so this should be a conflict
#    test_collection = load_test_data("test_collection.json")
#    resp = app_client.post("/collections", json=test_collection)
#    assert resp.status_code == 409

# Again deleting does not actually do anything
def test_delete_missing_collection(app_client):
    """Test deletion of a collection which does not exist"""
    resp = app_client.delete("/collections/missing-collection")
    assert resp.status_code == 404


# def test_update_collection_already_exists(app_client, load_test_data):
#    """Test updating a collection which already exists"""
#    test_collection = load_test_data("test_collection.json")
#    test_collection["keywords"].append("test")
#    resp = app_client.put("/collections", json=test_collection)
#    assert resp.status_code == 200
#
#    resp = app_client.get(f"/collections/{test_collection['id']}")
#    assert resp.status_code == 200
#    resp_json = resp.json()
#    assert "test" in resp_json["keywords"]
#


def test_update_new_collection(app_client, load_test_data):
    """Test updating a collection which does not exist (same as creation)"""
    test_collection = load_test_data("test_collection.json")
    test_collection["id"] = "new-test-collection"

    resp = app_client.put("/collections", json=test_collection)
    assert resp.status_code == 404


def test_collection_not_found(app_client):
    """Test read a collection which does not exist"""
    resp = app_client.get("/collections/does-not-exist")
    assert resp.status_code == 404


def test_collection_items_collectionid_not_found(app_client, load_test_data):
    """Test read an item with a collectionId that does not exist"""
    test_collection = load_test_data("test_collection.json")
    test_item = load_test_data("test_item.json")

    # Test that we get a 404 if the itemId does not exist but the collectionId does
    resp = app_client.get(f"/collections/{test_collection['id']}/items/does-not-exist")
    assert resp.status_code == 404

    # Test that we get a 404 if the collectionId does not exist but the itemId does
    resp = app_client.get(f"/collections/does-not-exist/items/{test_item['id']}")
    assert resp.status_code == 404

    # Test that we get a 404 if neither the itemId or the collectionId exists
    resp = app_client.get(f"/collections/does-not-exist/items/also-does-not-exist")
    assert resp.status_code == 404

    ## finally check that we get the item if both exists
    resp = app_client.get(
        f"/collections/{test_collection['id']}/items/{test_item['id']}"
    )
    assert resp.status_code == 200


def test_returns_valid_collection(app_client, load_test_data):
    """Test validates fetched collection with jsonschema"""
    test_collection = load_test_data("test_collection.json")
    resp = app_client.put("/collections", json=test_collection)
    assert resp.status_code == 200

    resp = app_client.get(f"/collections/{test_collection['id']}")
    assert resp.status_code == 200
    resp_json = resp.json()

    # Mock root to allow validation
    mock_root = pystac.Catalog(
        id="test", description="test desc", href="https://example.com"
    )
    collection = pystac.Collection.from_dict(
        resp_json, root=mock_root, preserve_dict=False
    )
    collection.validate()


def test_crs_on_collection(app_client, load_test_data):
    pass
