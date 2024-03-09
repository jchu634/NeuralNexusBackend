# from pathlib import Path
# import pytest
# import os

# # Test that the robots.txt is served correctly
# def test_get_robots_txt(client):
#     response = client.get('/robots.txt')

#     assert response.status_code == 200
#     assert response.headers['Content-Type'] in ['text/plain', 'text/plain; charset=utf-8']

# # Test that the favicon is served correctly
# def test_get_favicon(client):
#     response = client.get('/favicon.ico')

#     assert response.status_code == 200
#     assert response.headers['Content-Type'] in ['image/x-icon','image/vnd.microsoft.icon']

# # Test that the react build is served correctly
# def test_get_react_build(client):
#     responseHomepage = client.get('/')
#     responseUpload = client.get('/upload')

#     assert responseHomepage.status_code == 200
#     assert responseHomepage.headers['Content-Type'] == 'text/html; charset=utf-8'
#     assert responseUpload.status_code == 200
#     assert responseUpload.headers['Content-Type'] == 'text/html; charset=utf-8'

# # Test that the static files are served
# def test_get_static_files(client):
#     js_files = [f for f in Path("library/static/js").iterdir() if f.suffix == ".js"]
#     css_files = [f for f in Path("library/static/css").iterdir() if f.suffix == ".css"]

#     for file in js_files:
#         response = client.get(f'static/js/{file.name}')
#         assert response.status_code == 200
#         assert response.headers['Content-Type'] == 'application/javascript'

#     for file in css_files:
#         response = client.get(f'static/css/{file.name}')
#         assert response.status_code == 200
#         assert response.headers['Content-Type'] in ['text/css', 'text/css; charset=utf-8']

# # Test for directory traversal
# def test_get_static_files_sanitation(client):
#     response = client.get('static/../../config.py')

#     # The error is handled by serving the react page
#     assert response.status_code == 200
#     assert response.headers['Content-Type'] in ["text/html", "text/html; charset=utf-8"]


#     for f in [f for f in Path("library/static/js").iterdir() if f.suffix == ".js.map"]:
#         response = client.get(f'static/js/{f.name}')
#         assert response.status_code == 200
#         assert response.headers['Content-Type'] in ["text/html", "text/html; charset=utf-8"]
#         break

#     for f in [f for f in Path("library/static/css").iterdir() if f.suffix == ".css.map"]:
#         response = client.get(f'static/css/{f.name}')
#         assert response.status_code == 200
#         assert response.headers['Content-Type'] in ["text/html", "text/html; charset=utf-8"]
#         break
