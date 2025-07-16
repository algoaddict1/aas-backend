from flask import Blueprint, request, jsonify
from models import stories_collection, likes_collection, comments_collection, tips_collection
from bson import ObjectId
import datetime
from nft import mint_story_nft
import traceback  # ✅ per mostrare dettagli errore

routes = Blueprint("routes", __name__)

@routes.route("/stories", methods=["POST"])
def create_story():
    try:
        data = request.json
        print("📥 Dati ricevuti:", data)

        story_text = data["content"]
        wallet = data["wallet"]

        # 1. Salva la storia su MongoDB
        story = {
            "wallet": wallet,
            "content": story_text,
            "timestamp": datetime.datetime.utcnow()
        }
        result = stories_collection.insert_one(story)
        print("✅ Storia salvata con ID:", result.inserted_id)

        # 2. Mint dell’NFT su Algorand
        asset_id = mint_story_nft(story_text)
        print("🪙 NFT creato con ID:", asset_id)

        # 3. Aggiungi l'ID dell'NFT al documento
        stories_collection.update_one(
            {"_id": result.inserted_id},
            {"$set": {"nft_id": asset_id}}
        )

        return jsonify({
            "message": "Story saved & NFT minted!",
            "nft_id": asset_id
        }), 201

    except Exception as e:
        print("❌ ERRORE BACKEND POST /stories:", str(e))
        traceback.print_exc()  # ✅ stampa dettagliati
        return jsonify({
            "error": "Internal server error",
            "details": str(e)
        }), 500


@routes.route("/stories", methods=["GET"])
def get_stories():
    try:
        stories = list(stories_collection.find().sort("timestamp", -1))
        for s in stories:
            s["_id"] = str(s["_id"])
        return jsonify(stories)
    except Exception as e:
        print("❌ ERRORE BACKEND GET /stories:", str(e))
        traceback.print_exc()  # ✅
        return jsonify({"error": "Internal server error"}), 500


@routes.route("/like", methods=["POST"])
def like_story():
    try:
        data = request.json
        story_id = data["story_id"]
        wallet = data["wallet"]

        existing = likes_collection.find_one({"story_id": story_id, "wallet": wallet})
        if existing:
            return jsonify({"message": "Already liked"}), 400

        likes_collection.insert_one({"story_id": story_id, "wallet": wallet})
        return jsonify({"message": "Like registered", "cost": 500})
    except Exception as e:
        print("❌ ERRORE BACKEND /like:", str(e))
        traceback.print_exc()  # ✅
        return jsonify({"error": "Internal server error"}), 500


@routes.route("/comment", methods=["POST"])
def comment_story():
    try:
        data = request.json
        comment = {
            "story_id": data["story_id"],
            "wallet": data["wallet"],
            "text": data["text"],
            "timestamp": datetime.datetime.utcnow()
        }
        comments_collection.insert_one(comment)
        return jsonify({"message": "Comment saved", "cost": 500})
    except Exception as e:
        print("❌ ERRORE BACKEND /comment:", str(e))
        traceback.print_exc()  # ✅
        return jsonify({"error": "Internal server error"}), 500


@routes.route("/tip", methods=["POST"])
def tip_story():
    try:
        data = request.json
        tip = {
            "story_id": data["story_id"],
            "wallet": data["wallet"],
            "amount": data["amount"],
            "timestamp": datetime.datetime.utcnow()
        }
        tips_collection.insert_one(tip)
        return jsonify({"message": "Tip sent!"})
    except Exception as e:
        print("❌ ERRORE BACKEND /tip:", str(e))
        traceback.print_exc()  # ✅
        return jsonify({"error": "Internal server error"}), 500
