#!/usr/bin/python3
"""
API endpoints for managing 'Review' objects in a RESTful manner.
"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.review import Review
from models.place import Place
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """Returns a list of all Review objects for a given Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")
    reviews = place.reviews
    return jsonify([review.to_dict() for review in reviews])


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """Returns a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, "Review not found")
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """Deletes a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, "Review not found")

    storage.delete(review)
    storage.save()

    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """Creates a new Review for a given Place"""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404, "Place not found")

    review_data = request.get_json()
    if review_data is None:
        abort(400, "Not a JSON")

    if "user_id" not in review_data:
        abort(400, "Missing user_id")
    user = storage.get(User, review_data["user_id"])
    if user is None:
        abort(404, "User not found")

    if "text" not in review_data:
        abort(400, "Missing text")

    new_review = Review(
        text=review_data["text"],
        user_id=review_data["user_id"],
        place_id=place_id
    )
    storage.new(new_review)
    storage.save()

    return jsonify(new_review.to_dict()), 201


@app_views.route("/reviews/<review_id>", methods=["PUT"],
                 strict_slashes=False)
def update_review(review_id):
    """Updates a Review object by ID"""
    review = storage.get(Review, review_id)
    if review is None:
        abort(404, "Review not found")

    review_data = request.get_json()
    if review_data is None:
        abort(400, "Not a JSON")

    ignore_keys = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in review_data.items():
        if key not in ignore_keys:
            setattr(review, key, value)

    storage.save()
    return jsonify(review.to_dict()), 200
