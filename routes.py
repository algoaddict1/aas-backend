from flask import Blueprint, request, jsonify
from models import stories_collection, likes_collection, comments_collection, tips_collection
from bson import ObjectId
import datetime

routes = Blueprint("routes", __name__)

@routes.route("/stories", methods=["POST"])
def create_story():
    data = request.json
    story = {
        "wallet": data["wallet"],
        "content": data["content"],
        "timestamp": datetime.datetime.utcnow()
    }
    stories_collection.insert_one(story)
    return jsonify({"message": "Story saved!"}), 201

@routes.route("/stories", methods=["GET"])
def get_stories():
    stories = list(stories_collection.find().sort("timestamp", -1))
    for s in stories:
        s["_id"] = str(s["_id"])
    return jsonify(stories)

@routes.route("/like", methods=["POST"])
def like_story():
    data = request.json
    story_id = data["story_id"]
    wallet = data["wallet"]

    existing = likes_collection.find_one({"story_id": story_id, "wallet": wallet})
    if existing:
        return jsonify({"message": "Already liked"}), 400

    likes_collection.insert_one({"story_id": story_id, "wallet": wallet})
    return jsonify({"message": "Like registered", "cost": 500})

@routes.route("/comment", methods=["POST"])
def comment_story():
    data = request.json
    comment = {
        "story_id": data["story_id"],
        "wallet": data["wallet"],
        "text": data["text"],
        "timestamp": datetime.datetime.utcnow()
    }
    comments_collection.insert_one(comment)
    return jsonify({"message": "Comment saved", "cost": 500})

@routes.route("/tip", methods=["POST"])
def tip_story():
    data = request.json
    tip = {
        "story_id": data["story_id"],
        "wallet": data["wallet"],
        "amount": data["amount"],
        "timestamp": datetime.datetime.utcnow()
    }
    tips_collection.insert_one(tip)
    return jsonify({"message": "Tip sent!"})
