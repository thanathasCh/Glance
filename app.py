import os
import io
from common import config
from common import secret
from flask import Flask, request, send_file
from flask_cors import CORS
from cv import backend
from cv import image_processing as ip
from utility import background, remote
from utility.local import storage
# import sentry_sdk
# from sentry_sdk.integrations.flask import FlaskIntegratio

app = Flask(config.WEB_NAME)


@app.route('/')
def test():
    return 'Test'

@app.route('/test-model')
def embed_model():
    background._check_tasks_embed_model()
    return 'Done'

@app.route('/test-poc')
def index():
    background._check_tasks_poc()
    return 'Done'


@app.route('/load-products')
def load_products():
    # imagePaths = remote.get_unprocessed_product()
    imagePaths = remote.get_products_by_shelf(1)
    productIds = []
    productImages = []

    for imagePath in imagePaths:
        product_id = imagePath['id']

        try:
            image = remote.get_image(imagePath['imageUrl'])
        except:
            continue

        productIds.append(product_id)
        productImages.append(image)
        backend.add_fm_db(product_id, 0, image)

    backend.create_annoty_db(productIds, productImages, 0)
    remote.update_product_status(productIds)

    return 'finished'
    # try:
    #     imagePaths = remote.get_unprocessed_product()
    #     productIds = []
    #     productImages = []

    #     for imagePath in imagePaths:
    #         product_id = imagePath['id']
    #         image = remote.get_image(imagePath['imageUrl'])

    #         productIds.append(product_id)
    #         productImages.append(image)
    #         backend.add_fm_db(product_id, 0, image)

    #     backend.create_annoty_db(productImages, 0)
    #     remote.update_product_status(productIds)
    #     return 'finished'
    # except:
    #     return 'failed'


@app.route('/highlight-image', methods=['POST'])
def highlight_image():
    data = request.get_json()
    
    img = remote.get_image(data['imageUrl'])
    isGrouped = data['isGrouped']
    product_coords = data['productCoords']
    highlighted_img = ip.highlight_img(img, product_coords, isGrouped)

    return send_file(highlighted_img, mimetype='image/jpeg', as_attachment=True, attachment_filename='image.jpg')


@app.route('/highlight-empty-space', methods=['POST'])
def highlight_empty_space():
    data = request.get_json()

    img = remote.get_image(data['imageUrl'])
    product_coords = data['productCoords']
    highlighted_img = ip.highlight_empty_space(img, product_coords)

    return send_file(highlighted_img, mimetype='image/jpeg', as_attachment=True, attachment_filename='image.jpg')
# @app.route('/add_images', methods=['POST'])
# def add_images():
#     try:
#         ids = request.get_json()['ids']
#         images = remote.get_images(ids)
#         storage.add_feature(ids, images)
#     except:
#         return 'failed'
#     return 'finished'


# @app.route('/update_images', methods=['POST'])
# def update_images():
#     try:
#         ids = request.get_json()[ids]
#         images = remote.get_images(ids)
#         storage.update_feature(ids, images)
#     except:
#         return 'failed'
#     return 'finished'


# @app.route('/delete_images', methods=['POST'])
# def delete_images():
#     try:
#         ids = request.get_json()[ids]
#         images = remote.get_images(ids)
#         storage.delete_features(ids, images)
#     except:
#         return 'failed'
#     return 'finished'



# sentry_sdk.init(
#     dsn=secret.SENTRY_DNS,
#     integrations=[FlaskIntegration()],
#     traces_sample_rate=1.0
# )

# background.start()
app.run(debug=False)
CORS(app, support_credential=True)