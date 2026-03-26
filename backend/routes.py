from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################

@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################

@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    return make_response(jsonify(data), 200)

######################################################################
# GET A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    for picture in data:
        if picture['id'] == id:
            return make_response(jsonify(picture), 200)
    return make_response(jsonify(Message="Picture not found"), 404)


######################################################################
# CREATE A PICTURE
######################################################################

@app.route("/picture", methods=["POST"])
def create_picture():
    req = request.json
    print(f'post req: {req}')
    if picture_exists(req):
        id = req['id']
        return make_response(jsonify(Message=f'picture with id {id} already present'), 302)
    data.append(req)
    return make_response(jsonify(req), 201)


######################################################################
# UPDATE A PICTURE
######################################################################

@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id: int):
    req = request.json
    for i, item in enumerate(data):
        if item['id'] == id:
            if is_duplicate(item, req):
                return make_response(jsonify(Message=f"picture with id {picture['id']} already present"), 302)
            data[i] = req
            resp = make_response()
            resp.status_code = 200
            return resp
    return make_response(jsonify(Message="Picture Not Found"), 404)

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass


######################################################################
# Helper Methods
######################################################################
def picture_exists(pic: dict):
    for picture in data:
        if pic['id'] == picture['id']:
            return True
    return False

def is_duplicate(pic, incoming_pic):
    return pic['id'] == incoming_pic['id'] and pic['pic_url'] == incoming_pic['pic_url'] and pic['event_country'] == incoming_pic['event_country'] and pic['event_state'] == incoming_pic['event_state'] and pic['event_city'] == incoming_pic['event_city'] and pic['event_date'] == incoming_pic['event_date']
