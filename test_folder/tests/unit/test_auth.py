from pathlib import Path
import pytest
import os
from library import Settings

# Test authentication api


def test_create_user(client):
    client.post()
    images = [f for f in Path("testfiles")]

    with open():
        response = client.get('/api/v1/get_image?image_name=placeholder.png')

    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'image/png'

# Test that the image is served correctly after inference
# @pytest.mark.dependency(depends=["test_post_image"]])
# def test_get_image(client):
#     response = client.get('/api/v1/get_image?image_name=placeholder.png&hash=1')

#     assert response.status_code == 200
#     assert response.headers['Content-Type'] == 'image/png'

# Test for directory traversal


@pytest.mark.dependency(depends=["test_get_image"])
def test_get_image_sanitation(client):
    response = client.get('/api/v1/get_image?image_name=../../config.py&hash=')

    assert response.status_code == 200
    assert response.json() == {"error": "File not found"}

# Test that the available models are returned correctly


def test_get_available_models(client):
    subfolders = [os.path.basename(f.path)
                  for f in os.scandir(models_path) if f.is_dir()]
    response = client.get('/api/v1/available_models')

    assert response.status_code == 200
    assert response.json() == subfolders

# Test that a csv file is generated correctly if given valid json


@pytest.mark.dependency(depends=["test_post_image"])
@pytest.mark.skip(reason="No way of currently testing this")
def test_csv(client):
    pass
    # response = client.post(
    #     '/api/v1/create_csv',
    #     json={
    #         "name": "placeholder.png",

    #         "pred": {
    #             [
    #             "0.23":"class1",
    #             "0.2131231411":"class2",
    #             "362138148185":"class3",
    #             ]
    #         }
    #     }
    # )

    # assert response.status_code == 200
    # assert response.headers['Content-Type'] == "text/csv"

# Test that a csv file is generated correctly if given valid json


@pytest.mark.dependency(depends=["test_post_image"])
@pytest.mark.skip(reason="No way of currently testing this")
def test_xlsx(client):
    pass
    # response = client.post(
    #     '/api/v1/create_xlsx',
    #     json={
    #         "name": "placeholder.png",

    #         "pred": {
    #             [
    #             "0.23":"class1",
    #             "0.2131231411":"class2",
    #             "362138148185":"class3",
    #             ]
    #         }
    #     }
    # )

    # assert response.status_code == 200
    # assert response.headers['Content-Type'] == "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
