#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""COOKIE"""

import io
import os
import base64
from hashlib import md5
import requests
import magic
import json_log_formatter  # Used in gunicorn_logging.conf
from PIL import Image
from flask import (
    Flask,
    request,
    send_file,
    render_template,
    make_response,
    abort,
    jsonify,
    redirect,
    send_from_directory,
)

application = Flask(__name__, template_folder="templates")

# Fixed image width to scale to
application.config["COOKIE_FIXED_SIZE"] = int(os.environ.get("COOKIE_FIXED_SIZE", "120"))
# Scale percent
application.config["COOKIE_DEFAULT_SCALE"] = int(os.environ.get("COOKIE_DEFAULT_SCALE", "30"))
# Image size limit in bytes
application.config["COOKIE_IMAGE_MAX_SIZE"] = int(os.environ.get("COOKIE_IMAGE_MAX_SIZE", "31457280"))
# Max content length flask param 1024Mb
application.config["MAX_CONTENT_LENGTH"] = 1024 * 1024 * 1024
# Allowed mime types
application.config["COOKIE_ALLOWED_MIME"] = {}


def image_to_object(image):
    """convert image to Object"""
    try:
        file_object = io.BytesIO()
        image.save(file_object, image.format)
        file_object.seek(0)
        return file_object
    except:
        print("Error in image_to_object()")
        return abort(500)


def get_image_mime(stream):
    """Get Mime Type from stream"""
    try:
        mime = magic.from_buffer(stream.read(2048), mime=True)
        stream.seek(0)
        return mime
    except:
        print("Error in get_image_mime()")
        return abort(500)


def image_check(image_url):
    """Uploaded file checks"""
    try:
        headers = {"Range": "bytes=0-2048"}
        req = requests.get(image_url, headers=headers, allow_redirects=True, timeout=5)
        if req.status_code != 206:
            abort(req.status_code)
        content_length = int(req.headers.get("content-length", None))
        content_type = req.headers.get("content-type")
        image_head = io.BytesIO(req.content)
        mime = get_image_mime(image_head)  #get mime type from uploaded file
        if content_type != mime:
            abort(403, "Content missmatch")
        if content_length > application.config["COOKIE_IMAGE_MAX_SIZE"] :
            abort(403, "Image is too large")
#        if mime in application.config["COOKIE_ALLOWED_MIME"] = {}:
        return True
    except:
        print("Error in image_check()")
        return abort(500)

def md5hash(content):
    """image download by url and process"""
    return md5(content).hexdigest()

def image_process(image_url, scale_percent):
    """image download by url and process"""
    try:
        image_url = image_url.decode().rstrip("\n")
        if image_check(image_url):
            req = requests.get(image_url, allow_redirects=True, timeout=5)
            image = io.BytesIO(req.content)
            req.raw.decode_content = True
            thumb = make_thumbnail(image, scale_percent)
            return [ image_to_object(thumb), md5hash(req.content)]
        return abort(500)
    except:
        print("Error in image_process()")
        return abort(500)

def handle_scale(scale_percent):
    """handle scale percent"""
    try:
        if scale_percent != "" and scale_percent:
            if scale_percent != "fixed":
                scale_percent = int(scale_percent)
                if scale_percent <= 0 or scale_percent > 99:
                    return application.config["COOKIE_DEFAULT_SCALE"]
                return scale_percent
            return application.config["COOKIE_FIXED_SIZE"]
        return application.config["COOKIE_DEFAULT_SCALE"]
    except:
        print("Error in handle_scale()")
        return abort(500)


def make_thumbnail(input_image, scale_size):
    """make thumbnail image"""
    try:
        image = Image.open(input_image)
        width, height = image.size
        if scale_size != application.config["COOKIE_FIXED_SIZE"]:
            thumbsize = (((width / 100) * scale_size), ((height / 100) * scale_size))
            image.thumbnail(thumbsize, Image.ANTIALIAS)
            return image
        thumbsize = (scale_size, (height / (width / scale_size)))
        image.thumbnail(thumbsize, Image.ANTIALIAS)
        return image
    except:
        print("Error in make_thumbnail()")
        return abort(500)


@application.route("/", methods=["GET", "PUT"])
def req_handler():
    """GET/PUT requests handler"""
    try:
        if request.method == "GET":
            url = request.args.get("url")
            if url:
                url = base64.b64decode(url)
                scale_percent = request.args.get("scale")
                image_thumbnail, md5sum = image_process(url, handle_scale(scale_percent))
                response = make_response(send_file(image_thumbnail, mimetype="*/*"))
                response.headers['X-Orig-Hash'] = md5sum
                return response
        if request.method == "PUT":
            if "file" in request.files:
                file = request.files["file"]
                scale_percent = request.form.get("scale")
                image_thumbnail = image_to_object(make_thumbnail(file, handle_scale(scale_percent)))
                response = make_response(send_file(image_thumbnail, mimetype="*/*"))
                response.headers['X-Orig-Hash'] = md5hash(file.read())
                return response
        return redirect("/index.html", code=302)
    except:
        print("Error in req_handler()")
        return abort(500)

@application.errorhandler(405)
def method_forbidden(exception):
    """Method Not Allowed."""
    return jsonify(str(exception)), 405

@application.errorhandler(404)
def resource_not_found(exception):
    """Page not found."""
    return jsonify(str(exception)), 404

@application.errorhandler(403)
def resource_forbidden(exception):
    """Forbidden."""
    return jsonify(str(exception)), 403

@application.errorhandler(500)
def resource_error(exception):
    """Internal Error."""
    return jsonify(str(exception)), 500

@application.route("/index.html")
def default_index():
    """Index page"""
    return make_response(render_template("index.html"), 200)

@application.route("/favicon.ico")
def favicon():
    """favicon.ico"""
    return send_from_directory(
        os.path.join(application.root_path, "static"),
        "favicon.ico",
        mimetype="image/vnd.microsoft.icon",
    )

if __name__ == "__main__":
    application.run(threaded=True)
