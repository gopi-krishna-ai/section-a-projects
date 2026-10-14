"""
AgriMitra AI - Multilingual AI Assistant for Crop and Fertilizer Recommendation

Flask application entry point.
"""

import os
from datetime import datetime

from dotenv import load_dotenv
from flask import (
    Flask,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
from werkzeug.security import check_password_hash, generate_password_hash

from assistant import get_assistant_reply
from ml.predict import (
    ModelLoadError,
    crop_model_info,
    fertilizer_categories,
    fertilizer_model_info,
    predict_crop,
    predict_fertilizer,
)
from translator import translate_text, translate_texts

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "agrimitra-dev-secret-change-me")

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
database_dir = os.path.join(BASE_DIR, "database")
os.makedirs(database_dir, exist_ok=True)
# Overridable via env so the test suite can use a throwaway database.
db_path = os.environ.get("AGRIMITRA_DB_PATH") or os.path.join(database_dir, "agrimitra.db")

app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

SUPPORTED_LANGUAGES = ["en", "kn", "hi", "te", "ta"]


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    fullname = db.Column(db.String(100), nullable=False)
    userid = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15))
    password = db.Column(db.String(255), nullable=False)
    language = db.Column(db.String(20), default="en")



class Product(db.Model):
    __tablename__ = "products"
    id = db.Column(db.Integer, primary_key=True)
    item_type = db.Column(db.String(50), nullable=False) # 'seed' or 'fertilizer'
    item_name = db.Column(db.String(100), nullable=False) # e.g. 'Coffee', 'Rice', '10-26-26'
    seller = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    stock = db.Column(db.Integer, default=100)
    discount = db.Column(db.Integer, default=0)



class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default='Pending Approval')
    delivery_address = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class OrderItem(db.Model):
    __tablename__ = "order_items"
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey("orders.id"), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey("products.id"), nullable=False)
    quantity = db.Column(db.Float, nullable=False)
    price = db.Column(db.Float, nullable=False)

class PredictionHistory(db.Model):
    __tablename__ = "prediction_history"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    language = db.Column(db.String(20), default="en")
    crop_inputs = db.Column(db.JSON)
    predicted_crop = db.Column(db.String(100))
    crop_confidence = db.Column(db.Float)
    fertilizer_inputs = db.Column(db.JSON)
    recommended_fertilizer = db.Column(db.String(100))
    fertilizer_confidence = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)


with app.app_context():
    db.create_all()
    print("\n==============================")
    print("AgriMitra AI Database")
    print("==============================")
    print("Database Path:", db_path)
    print("Tables:", inspect(db.engine).get_table_names())
    print("==============================\n")


# ---------------------------------------------------------------------------

import werkzeug
import os
from werkzeug.utils import secure_filename

app.config['UPLOAD_FOLDER'] = os.path.join(BASE_DIR, 'static', 'uploads')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route("/api/products", methods=["GET"])
def get_products():
    products = Product.query.all()
    return jsonify([{
        "id": p.id,
        "item_type": p.item_type,
        "item_name": p.item_name,
        "seller": p.seller,
        "description": p.description,
        "price": p.price,
        "image_url": p.image_url
    } for p in products])

# Helpers
# ---------------------------------------------------------------------------


def login_required(view):
    """Simple login gate for page routes."""

    def wrapped(*args, **kwargs):
        if "user_id" not in session:
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    wrapped.__name__ = view.__name__
    return wrapped


@app.context_processor
def inject_user():
    return dict(current_user=get_logged_in_user())

def get_logged_in_user():
    if "user_id" not in session:
        return None
    return db.session.get(User, session["user_id"])


def current_language(user=None):
    lang = session.get("language") or (user.language if user else None) or "en"
    return lang if lang in SUPPORTED_LANGUAGES else "en"


def parse_float(value, field_name):
    """Parses a form value into float with a clear error message."""
    if value is None or str(value).strip() == "":
        raise ValueError(f"Please enter a value for '{field_name}'.")
    try:
        return float(value)
    except (TypeError, ValueError):
        raise ValueError(f"'{field_name}' must be a number.")


def first_present(*values):
    """Returns the first value that is not None and not an empty string.
    Unlike 'a or b', this keeps valid falsy values like 0."""
    for value in values:
        if value is not None and str(value).strip() != "":
            return value
    return None


def validate_ranges(inputs, rules):
    """
    Checks numeric inputs against (min, max) rules.
    rules: {key: (min, max, message)}. A None bound means unlimited.
    """
    for key, (lo, hi, message) in rules.items():
        value = float(inputs[key])
        if lo is not None and value < lo:
            raise ValueError(message)
        if hi is not None and value > hi:
            raise ValueError(message)


def save_history(user, language, crop_result=None, fert_result=None):
    entry = PredictionHistory(
        user_id=user.id,
        language=language,
        crop_inputs=crop_result["input_features"] if crop_result else None,
        predicted_crop=crop_result["crop"] if crop_result else None,
        crop_confidence=crop_result["confidence"] if crop_result else None,
        fertilizer_inputs=fert_result["input_features"] if fert_result else None,
        recommended_fertilizer=fert_result["fertilizer"] if fert_result else None,
        fertilizer_confidence=fert_result["confidence"] if fert_result else None,
    )
    db.session.add(entry)
    db.session.commit()


# ---------------------------------------------------------------------------
# Public pages
# ---------------------------------------------------------------------------


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/splash")
def splash():
    return render_template("splash.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    lang = request.args.get("lang", "en")
    if lang not in SUPPORTED_LANGUAGES:
        lang = "en"

    if request.method == "POST":
        # Accept both JSON requests (fetch/AJAX) and normal HTML form posts.
        data = request.get_json(silent=True)
        if not data:
            data = request.form.to_dict()

        userid = str(data.get("userid", "")).strip()
        password = str(data.get("password", ""))
        selected_language = str(data.get("language", "")).strip()

        if not userid:
            return jsonify({
                "success": False,
                "message": "Enter correct User ID."
            }), 400

        if not password:
            return jsonify({
                "success": False,
                "message": "Enter valid password."
            }), 400

        user = User.query.filter_by(userid=userid).first()

        # Check the User ID first so the UI can show a useful message.
        if not user:
            return jsonify({
                "success": False,
                "message": "Enter correct User ID."
            }), 401

        # Then verify the password against the hashed password saved at registration.
        if not check_password_hash(user.password, password):
            return jsonify({
                "success": False,
                "message": "Enter valid password."
            }), 401

        # Login successful: create the session used by @login_required.
        session["user_id"] = user.id
        session["language"] = (
            selected_language
            if selected_language in SUPPORTED_LANGUAGES
            else (user.language if user.language in SUPPORTED_LANGUAGES else "en")
        )

        user.language = session["language"]
        db.session.commit()

        return jsonify({
            "success": True,
            "message": "Login successful.",
            "redirect": url_for("dashboard")
        })

    return render_template("login.html", language=lang)


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    # Accept both JSON requests and normal HTML form posts.
    data = request.get_json(silent=True)
    if not data:
        data = request.form.to_dict()

    if not data:
        return jsonify({"success": False, "message": "Invalid request"}), 400

    fullname = data.get("fullname", "").strip()
    userid = data.get("userid", "").strip()
    email = data.get("email", "").strip().lower()
    phone = data.get("phone", "").strip()
    password = data.get("password", "")
    language = data.get("language", "en")
    if language not in SUPPORTED_LANGUAGES:
        language = "en"

    if not fullname or not userid or not email or not password:
        return jsonify({
            "success": False,
            "message": "Please fill all required fields."
        }), 400

    if len(password) < 6:
        return jsonify({
            "success": False,
            "message": "Password must contain at least 6 characters."
        }), 400

    existing_user = User.query.filter_by(userid=userid).first()
    if existing_user:
        return jsonify({
            "success": False,
            "message": "User ID already exists."
        }), 409

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({
            "success": False,
            "message": "Email already registered."
        }), 409

    hashed_password = generate_password_hash(password)
    new_user = User(
        fullname=fullname,
        userid=userid,
        email=email,
        phone=phone,
        password=hashed_password,
        language=language,
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Registration successful.",
        "userid": userid
    })


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


# ---------------------------------------------------------------------------
# Authenticated pages
# ---------------------------------------------------------------------------


@app.route("/dashboard")
@login_required
def dashboard():
    user = get_logged_in_user()
    return render_template("dashboard.html", user=user, language=current_language(user), active_page="dashboard")


@app.route("/crop")
@login_required
def crop_page():
    user = get_logged_in_user()
    return render_template("recommendation.html", user=user, language=current_language(user), active_page="crop", active_mode="crop")


@app.route("/fertilizer")
@login_required
def fertilizer_page():
    user = get_logged_in_user()
    active_mode = "fertilizer"
    return render_template("recommendation.html", user=user, language=current_language(user), active_page="fertilizer", active_mode=active_mode)


@app.route("/recommendation")
@login_required
def recommendation_page():
    user = get_logged_in_user()
    last_crop_pred = PredictionHistory.query.filter_by(user_id=user.id).filter(PredictionHistory.predicted_crop != None).order_by(PredictionHistory.created_at.desc()).first()
    last_fert_pred = PredictionHistory.query.filter_by(user_id=user.id).filter(PredictionHistory.recommended_fertilizer != None).order_by(PredictionHistory.created_at.desc()).first()
    
    crop = last_crop_pred.predicted_crop if last_crop_pred else "Rice"
    fert = last_fert_pred.recommended_fertilizer if last_fert_pred else "Urea"
    
    soil_score = 85
    soil_label = "Good"
    
    inputs = {}
    if last_crop_pred and last_crop_pred.crop_inputs:
        inputs.update(last_crop_pred.crop_inputs)
    if last_fert_pred and last_fert_pred.fertilizer_inputs:
        inputs.update(last_fert_pred.fertilizer_inputs)
        
    if inputs:
        n = float(inputs.get("nitrogen") or 50)
        p = float(inputs.get("phosphorus") or inputs.get("phosphorous") or 50)
        k = float(inputs.get("potassium") or 50)
        ph = float(inputs.get("ph") or 7.0)
        
        score = 100
        if n < 40 or n > 120: score -= 15
        if p < 15 or p > 60: score -= 15
        if k < 15 or k > 60: score -= 15
        if ph < 5.5 or ph > 8.0: score -= 20
        
        soil_score = max(0, min(100, int(score)))
        if soil_score >= 80: soil_label = "Excellent"
        elif soil_score >= 60: soil_label = "Good"
        elif soil_score >= 40: soil_label = "Fair"
        else: soil_label = "Poor"
            
    return render_template("report.html", user=user, language=current_language(user), active_page="recommendation", crop=crop, fert=fert, soil_score=soil_score, soil_label=soil_label)


@app.route("/lifecycle")
@login_required
def lifecycle_page():
    user = get_logged_in_user()
    
    crop = request.args.get("crop")
    fert = None
    if not crop:
        last_crop_pred = PredictionHistory.query.filter_by(user_id=user.id).filter(PredictionHistory.predicted_crop != None).order_by(PredictionHistory.created_at.desc()).first()
        last_fert_pred = PredictionHistory.query.filter_by(user_id=user.id).filter(PredictionHistory.recommended_fertilizer != None).order_by(PredictionHistory.created_at.desc()).first()
        
        if last_crop_pred: crop = last_crop_pred.predicted_crop
        if last_fert_pred: fert = last_fert_pred.recommended_fertilizer
    
    if not crop: crop = "Rice"
    if not fert: fert = "Urea"

    return render_template("lifecycle.html", user=user, language=current_language(user), active_page="lifecycle", crop=crop, fert=fert)


@app.route("/market")
@login_required
def market_page():
    user = get_logged_in_user()
    
    crop = request.args.get("crop")
    if not crop:
        last_crop_pred = PredictionHistory.query.filter_by(user_id=user.id).filter(PredictionHistory.predicted_crop != None).order_by(PredictionHistory.created_at.desc()).first()
        if last_crop_pred:
            crop = last_crop_pred.predicted_crop
        else:
            crop = "Rice"
            
    lat = request.args.get("lat", "20.5937")
    lon = request.args.get("lon", "78.9629")
    return render_template("market.html", user=user, language=current_language(user), active_page="market", crop=crop, lat=lat, lon=lon)


@app.route("/soil")
@login_required
def soil_page():
    user = get_logged_in_user()
    return render_template("recommendation.html", user=user, language=current_language(user), active_page="soil", active_mode="soil")


@app.route("/assistant")
@login_required
def assistant_page():
    user = get_logged_in_user()
    return render_template("assistant.html", user=user, language=current_language(user), active_page="assistant")


@app.route("/history")
@login_required
def history_page():
    user = get_logged_in_user()
    return render_template("history.html", user=user, language=current_language(user), active_page="history")


@app.route("/profile")
@login_required
def profile_page():
    user = get_logged_in_user()
    return render_template("profile.html", user=user, language=current_language(user), active_page="profile")


@app.route("/settings")
@login_required
def settings_page():
    user = get_logged_in_user()
    return render_template("settings.html", user=user, language=current_language(user), active_page="settings")


# ---------------------------------------------------------------------------
# Language
# ---------------------------------------------------------------------------


@app.route("/api/language", methods=["POST"])
def api_language():
    """Persists the selected interface language so the choice survives
    navigation. Works pre-login too (session) and updates the user's
    preferred language when logged in."""
    data = request.get_json(silent=True) or {}
    lang = str(data.get("language", "")).strip()

    if lang not in SUPPORTED_LANGUAGES:
        return jsonify({"success": False, "message": "Unsupported language."}), 400

    session["language"] = lang

    user = get_logged_in_user()
    if user:
        user.language = lang
        db.session.commit()

    return jsonify({"success": True, "language": lang})


# ---------------------------------------------------------------------------
# Translation
# ---------------------------------------------------------------------------


@app.route("/translate", methods=["POST"])
def translate():
    data = request.get_json(silent=True) or {}
    language = data.get("language", "en")

    texts = data.get("texts")
    if isinstance(texts, list):
        return jsonify({"translations": translate_texts([str(t) for t in texts], language)})

    text = data.get("text", "")
    return jsonify({"translated": translate_text(text, language)})


# ---------------------------------------------------------------------------
# ML prediction APIs
# ---------------------------------------------------------------------------


def build_crop_inputs(data):
    """Reads and validates the 7 crop-model features from a JSON payload."""
    inputs = {
        "nitrogen": parse_float(data.get("nitrogen"), "Nitrogen (N)"),
        "phosphorus": parse_float(first_present(data.get("phosphorus"), data.get("phosphorous")), "Phosphorus (P)"),
        "potassium": parse_float(data.get("potassium"), "Potassium (K)"),
        "temperature": parse_float(data.get("temperature"), "Temperature"),
        "humidity": parse_float(data.get("humidity"), "Humidity"),
        "ph": parse_float(data.get("ph"), "pH"),
        "rainfall": parse_float(data.get("rainfall"), "Rainfall"),
    }
    validate_ranges(inputs, {
        "nitrogen": (0, None, "Nitrogen cannot be negative."),
        "phosphorus": (0, None, "Phosphorus cannot be negative."),
        "potassium": (0, None, "Potassium cannot be negative."),
        "temperature": (-10, 60, "Temperature should be between -10 and 60 °C."),
        "humidity": (0, 100, "Humidity should be between 0 and 100%."),
        "ph": (0, 14, "pH should be between 0 and 14."),
        "rainfall": (0, None, "Rainfall cannot be negative."),
    })
    return inputs


@app.route("/api/crop", methods=["POST"])
def api_crop():
    data = request.get_json(silent=True) or {}
    try:
        inputs = build_crop_inputs(data)
        result = predict_crop(inputs)
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc)}), 400
    except ModelLoadError as exc:
        return jsonify({"success": False, "message": str(exc)}), 503
    except Exception as exc:
        app.logger.error("Crop prediction failed: %s", exc)
        return jsonify({"success": False, "message": "Prediction failed. Please try again."}), 500

    user = get_logged_in_user()
    if user:
        try:
            save_history(user, current_language(user), crop_result=result)
        except Exception as exc:
            app.logger.error("History save failed: %s", exc)

    result["success"] = True
    return jsonify(result)


def build_fertilizer_inputs(data):
    """Reads and validates the fertilizer-model features from a JSON payload."""
    inputs = {
        "temperature": parse_float(data.get("temperature"), "Temperature"),
        "humidity": parse_float(data.get("humidity"), "Humidity"),
        "moisture": parse_float(data.get("moisture"), "Soil Moisture"),
        "soil_type": str(data.get("soil_type", "")).strip(),
        "crop_type": str(data.get("crop_type", "")).strip(),
        "nitrogen": parse_float(data.get("nitrogen"), "Nitrogen (N)"),
        "potassium": parse_float(data.get("potassium"), "Potassium (K)"),
        "phosphorous": parse_float(first_present(data.get("phosphorous"), data.get("phosphorus")), "Phosphorous (P)"),
    }
    validate_ranges(inputs, {
        "temperature": (-10, 60, "Temperature should be between -10 and 60 °C."),
        "humidity": (0, 100, "Humidity should be between 0 and 100%."),
        "moisture": (0, 100, "Moisture should be between 0 and 100%."),
        "nitrogen": (0, None, "Nitrogen cannot be negative."),
        "potassium": (0, None, "Potassium cannot be negative."),
        "phosphorous": (0, None, "Phosphorous cannot be negative."),
    })
    return inputs


@app.route("/api/fertilizer", methods=["POST"])
def api_fertilizer():
    data = request.get_json(silent=True) or {}
    try:
        inputs = build_fertilizer_inputs(data)
        result = predict_fertilizer(inputs)
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc)}), 400
    except ModelLoadError as exc:
        return jsonify({"success": False, "message": str(exc)}), 503
    except Exception as exc:
        app.logger.error("Fertilizer prediction failed: %s", exc)
        return jsonify({"success": False, "message": "Prediction failed. Please try again."}), 500

    user = get_logged_in_user()
    if user:
        try:
            save_history(user, current_language(user), fert_result=result)
        except Exception as exc:
            app.logger.error("History save failed: %s", exc)

    result["success"] = True
    return jsonify(result)


# Mapping between crop-model outputs and fertilizer-model crop types.
# Only meaningful matches are included; the UI lets the user pick otherwise.
CROP_TO_FERTILIZER_CROP = {
    "Rice": "Paddy",
    "Maize": "Maize",
    "Cotton": "Cotton",
    "Blackgram": "Pulses",
    "ChickPea": "Pulses",
    "KidneyBeans": "Pulses",
    "Lentil": "Pulses",
    "MothBeans": "Pulses",
    "MungBean": "Pulses",
    "PigeonPeas": "Pulses",
}


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    """Combined workflow: crop prediction -> fertilizer recommendation."""
    data = request.get_json(silent=True) or {}

    try:
        crop_inputs = build_crop_inputs(data)
        crop_result = predict_crop(crop_inputs)

        suggested_crop_type = CROP_TO_FERTILIZER_CROP.get(crop_result["crop"])
        if not suggested_crop_type:
            # The crop model's own output may itself be a valid fertilizer crop type
            # (e.g. Maize, Cotton), so use it directly when that is the case.
            if crop_result["crop"] in fertilizer_categories()["crop_types"]:
                suggested_crop_type = crop_result["crop"]

        if suggested_crop_type:
            data["crop_type"] = suggested_crop_type
        elif not str(data.get("crop_type", "")).strip():
            return jsonify({
                "success": False,
                "message": (
                    f"The predicted crop '{crop_result['crop']}' does not map to a "
                    "fertilizer crop type. Please select a crop type for the "
                    "fertilizer model."
                )
            }), 400

        fert_inputs = build_fertilizer_inputs(data)
        fert_result = predict_fertilizer(fert_inputs)
    except ValueError as exc:
        return jsonify({"success": False, "message": str(exc)}), 400
    except ModelLoadError as exc:
        return jsonify({"success": False, "message": str(exc)}), 503
    except Exception as exc:
        app.logger.error("Combined prediction failed: %s", exc)
        return jsonify({"success": False, "message": "Prediction failed. Please try again."}), 500

    user = get_logged_in_user()
    if user:
        try:
            save_history(
                user,
                current_language(user),
                crop_result=crop_result,
                fert_result=fert_result,
            )
        except Exception as exc:
            app.logger.error("History save failed: %s", exc)

    return jsonify({
        "success": True,
        "crop": crop_result["crop"],
        "crop_confidence": crop_result["confidence"],
        "fertilizer": fert_result["fertilizer"],
        "fertilizer_confidence": fert_result["confidence"],
        "used_crop_type": suggested_crop_type,
        "crop_inputs": crop_inputs,
        "fertilizer_inputs": fert_inputs,
    })


@app.route("/api/fertilizer/meta", methods=["GET"])
def api_fertilizer_meta():
    """Returns the categorical values the fertilizer model was trained on."""
    try:
        info = fertilizer_model_info()
        cats = fertilizer_categories()
        return jsonify({
            "success": True,
            "soil_types": cats["soil_types"],
            "crop_types": cats["crop_types"],
            "fertilizers": info["classes"],
        })
    except Exception as exc:
        app.logger.error("Fertilizer meta failed: %s", exc)
        return jsonify({"success": False, "message": "Model metadata unavailable."}), 503


@app.route("/api/model-info", methods=["GET"])
def api_model_info():
    """Model metadata for the UI (accuracy as actually measured at training time)."""
    try:
        crop_info = crop_model_info()
        fert_info = fertilizer_model_info()
        return jsonify({
            "success": True,
            "crop": crop_info,
            "fertilizer": fert_info,
        })
    except Exception:
        return jsonify({"success": False, "message": "Model metadata unavailable."}), 503


# ---------------------------------------------------------------------------
# AI Assistant
# ---------------------------------------------------------------------------


@app.route("/api/assistant", methods=["POST"])
def api_assistant():
    data = request.get_json(silent=True) or {}
    question = str(data.get("question", "")).strip()
    language = data.get("language", "en")
    if language not in SUPPORTED_LANGUAGES:
        language = "en"

    if not question:
        return jsonify({
            "success": False,
            "message": "Please type or speak a question."
        }), 400

    try:
        from translator import translate_to_english
        english_question = translate_to_english(question)
        
        # Intercept specific predefined questions to answer "from memory"
        eq_lower = english_question.lower().strip()
        user = get_logged_in_user()
        memory_reply = None
        
        if user:
            if "which crop" in eq_lower and "soil" in eq_lower:
                last_crop_pred = PredictionHistory.query.filter_by(user_id=user.id).filter(PredictionHistory.predicted_crop != None).order_by(PredictionHistory.created_at.desc()).first()
                if last_crop_pred:
                    c_inputs = last_crop_pred.crop_inputs or {}
                    n = c_inputs.get("Nitrogen", 0)
                    p = c_inputs.get("Phosphorus", 0)
                    k = c_inputs.get("Potassium", 0)
                    ph = c_inputs.get("pH_Value", 6.5)
                    crop_name = last_crop_pred.predicted_crop
                    memory_reply = f"Based on your latest soil test (N: {n}, P: {p}, K: {k}, pH: {ph}), I recommend growing **{crop_name}**. This crop will thrive in your soil conditions!"
            elif "irrigate" in eq_lower or "water" in eq_lower:
                last_crop_pred = PredictionHistory.query.filter_by(user_id=user.id).filter(PredictionHistory.predicted_crop != None).order_by(PredictionHistory.created_at.desc()).first()
                if last_crop_pred and last_crop_pred.predicted_crop:
                    crop = last_crop_pred.predicted_crop
                    memory_reply = f"Since you are growing **{crop}**, you should irrigate early in the morning. Make sure to monitor the soil moisture closely, as {crop} requires consistent watering but not waterlogging."
            elif "pest" in eq_lower or "control" in eq_lower:
                last_crop_pred = PredictionHistory.query.filter_by(user_id=user.id).filter(PredictionHistory.predicted_crop != None).order_by(PredictionHistory.created_at.desc()).first()
                if last_crop_pred and last_crop_pred.predicted_crop:
                    crop = last_crop_pred.predicted_crop
                    memory_reply = f"For your **{crop}** field, inspect the leaves regularly. If you see pests, start with neem-based sprays as an organic first line of defense before using chemical pesticides."

        if memory_reply:
            reply = memory_reply
            source = "memory"
        else:
            reply, source = get_assistant_reply(english_question, language)
        
        # LLM replies already come back in the requested language (when the API
        # key is configured); only translate knowledge-base / fallback replies.
        if source == "llm":
            translated = reply
        else:
            translated = translate_text(reply, language)
        return jsonify({
            "success": True,
            "reply": translated,
            "english_reply": reply,
            "source": source,
        })
    except Exception as exc:
        app.logger.error("Assistant failed: %s", exc)
        return jsonify({
            "success": False,
            "message": "Sorry, the assistant is unavailable right now. Please try again."
        }), 500


# ---------------------------------------------------------------------------
# History / Profile / Settings
# ---------------------------------------------------------------------------


@app.route("/api/history", methods=["GET"])
@login_required
def api_history():
    user = get_logged_in_user()
    rows = (
        PredictionHistory.query.filter_by(user_id=user.id)
        .order_by(PredictionHistory.created_at.desc())
        .limit(50)
        .all()
    )
    items = []
    for r in rows:
        items.append({
            "id": r.id,
            "created_at": r.created_at.strftime("%d %b %Y, %I:%M %p") if r.created_at else "",
            "language": r.language,
            "predicted_crop": r.predicted_crop,
            "crop_confidence": r.crop_confidence,
            "recommended_fertilizer": r.recommended_fertilizer,
            "fertilizer_confidence": r.fertilizer_confidence,
        })
    return jsonify({"success": True, "history": items})


@app.route("/api/profile", methods=["POST"])
@login_required
def api_profile():
    user = get_logged_in_user()
    data = request.get_json(silent=True) or {}

    phone = str(data.get("phone", "")).strip()
    language = data.get("language", "")

    if language in SUPPORTED_LANGUAGES:
        user.language = language
        session["language"] = language

    user.phone = phone
    db.session.commit()
    return jsonify({"success": True, "message": "Profile updated."})


@app.route("/api/settings", methods=["POST"])
@login_required
def api_settings():
    user = get_logged_in_user()
    data = request.get_json(silent=True) or {}

    language = data.get("language", "")
    if language in SUPPORTED_LANGUAGES:
        user.language = language
        session["language"] = language

    current_password = str(data.get("current_password", ""))
    new_password = str(data.get("new_password", ""))

    if new_password:
        if not check_password_hash(user.password, current_password):
            return jsonify({
                "success": False,
                "message": "Current password is incorrect."
            }), 400
        if len(new_password) < 6:
            return jsonify({
                "success": False,
                "message": "New password must contain at least 6 characters."
            }), 400
        user.password = generate_password_hash(new_password)

    db.session.commit()
    return jsonify({"success": True, "message": "Settings saved."})


# ---------------------------------------------------------------------------
# Weather proxy (server-side so no API key is exposed to the browser)
# ---------------------------------------------------------------------------


@app.route("/api/weather", methods=["GET"])
def api_weather():
    lat = request.args.get("lat", "20.5937") # Default India
    lon = request.args.get("lon", "78.9629")

    try:
        import urllib.request
        import urllib.parse
        import json
        
        base_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,surface_pressure,wind_speed_10m",
            "timezone": "auto"
        }
        url = base_url + "?" + urllib.parse.urlencode(params)
        
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read().decode())
        
        if "current" in data:
            current = data["current"]
            
            # Map weather code to condition
            wmo = current.get("weather_code", 0)
            condition = "Sunny"
            icon = "/static/images/real_sun.jpg"
            
            if wmo in [1, 2, 3]:
                condition = "Cloudy"
                icon = "//cdn.weatherapi.com/weather/64x64/day/119.png" # generic cloud
            elif wmo in [45, 48]:
                condition = "Fog"
                icon = "//cdn.weatherapi.com/weather/64x64/day/143.png"
            elif wmo in [51, 53, 55, 56, 57]:
                condition = "Drizzle"
                icon = "//cdn.weatherapi.com/weather/64x64/day/266.png"
            elif wmo in [61, 63, 65, 66, 67, 80, 81, 82]:
                condition = "Rain"
                icon = "//cdn.weatherapi.com/weather/64x64/day/308.png"
            elif wmo in [71, 73, 75, 77, 85, 86]:
                condition = "Snow"
                icon = "//cdn.weatherapi.com/weather/64x64/day/338.png"
            elif wmo >= 95:
                condition = "Thunderstorm"
                icon = "//cdn.weatherapi.com/weather/64x64/day/386.png"

            return jsonify({
                "success": True,
                "live": True,
                "temperature": current.get("temperature_2m", 0),
                "condition": condition,
                "icon": icon,
                "humidity": current.get("relative_humidity_2m", 0),
                "wind": current.get("wind_speed_10m", 0),
                "rain": current.get("precipitation", 0),
                "uv": 5, # Open-Meteo requires daily for UV, keeping hardcoded or static for simplicity
                "pressure": current.get("surface_pressure", 1012),
                "visibility": 10, # Not all regions have visibility
                "feels_like": current.get("apparent_temperature", 0),
                "updated": data.get("current", {}).get("time", "Live").replace("T", " ")
            })
    except Exception as exc:
        app.logger.warning("Weather API failed: %s", exc)

    # Demo fallback if open-meteo fails
    return jsonify({
        "success": True,
        "live": False,
        "temperature": 29,
        "condition": "Sunny",
        "icon": "/static/images/real_sun.jpg",
        "humidity": 68,
        "wind": 12,
        "rain": 0,
        "uv": 6,
        "pressure": 1012,
        "visibility": 10,
        "feels_like": 31,
        "updated": "demo",
    })


# ---------------------------------------------------------------------------
# Error handling
# ---------------------------------------------------------------------------


@app.errorhandler(404)
def not_found(error):
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "message": "Not found."}), 404
    return render_template("error.html", code=404, message="Page not found."), 404


@app.errorhandler(500)
def internal_error(error):
    app.logger.error("Internal error: %s", error)
    if request.path.startswith("/api/"):
        return jsonify({"success": False, "message": "Something went wrong on the server."}), 500
    return render_template("error.html", code=500, message="Something went wrong on the server."), 500


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/admin/login")
def admin_login_page():
    return render_template("admin_login.html")

@app.route("/api/admin/login", methods=["POST"])
def api_admin_login():
    data = request.get_json(silent=True) or {}
    userid = str(data.get("userid", "")).strip()
    password = str(data.get("password", ""))
    
    if userid != 'admin@agrimitra':
        return jsonify({"success": False, "message": "Invalid admin credentials."}), 401
        
    user = User.query.filter_by(userid=userid).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"success": False, "message": "Invalid admin credentials."}), 401
        
    session["user_id"] = user.id
    session["language"] = user.language
    return jsonify({"success": True})

@app.route("/admin")
@login_required
def admin_dashboard():
    user = get_logged_in_user()
    if user.userid != "admin@agrimitra":
        return redirect(url_for("admin_login_page"))
    return render_template("admin.html")


@app.route("/api/admin/product", methods=["POST"])
@login_required
def add_product():
    user = get_logged_in_user()
    if user.userid != "admin@agrimitra":
        return jsonify({"success": False, "message": "Access Denied"}), 403
    try:
        item_type = request.form.get("item_type")
        item_name = request.form.get("item_name")
        seller = request.form.get("seller")
        description = request.form.get("description")
        price = float(request.form.get("price"))
        stock = int(request.form.get("stock", 100))
        discount = int(request.form.get("discount", 0))
        
        file = request.files.get("image")
        image_url = ""
        if file and file.filename:
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            image_url = f"/static/uploads/{filename}"
        else:
            image_url = request.form.get("image_url", "")

        product = Product(
            item_type=item_type,
            item_name=item_name,
            seller=seller,
            description=description,
            price=price,
            image_url=image_url,
            stock=stock,
            discount=discount
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({"success": True, "message": "Product added successfully!"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 400



@app.route("/api/admin/product/<int:product_id>", methods=["DELETE"])
@login_required
def delete_product(product_id):
    if get_logged_in_user().userid != "admin@agrimitra": return jsonify({"success": False}), 403
    p = Product.query.get_or_404(product_id)
    db.session.delete(p)
    db.session.commit()
    return jsonify({"success": True})

@app.route("/api/admin/product/<int:product_id>", methods=["PUT"])
@login_required
def update_product(product_id):
    if get_logged_in_user().userid != "admin@agrimitra": return jsonify({"success": False}), 403
    p = Product.query.get_or_404(product_id)
    data = request.get_json(silent=True) or {}
    if 'price' in data: p.price = float(data['price'])
    if 'stock' in data: p.stock = int(data['stock'])
    if 'discount' in data: p.discount = int(data['discount'])
    if 'description' in data: p.description = data['description']
    db.session.commit()
    return jsonify({"success": True})

@app.route("/api/admin/orders", methods=["GET"])
@login_required
def get_orders():
    if get_logged_in_user().userid != "admin@agrimitra": return jsonify({"success": False}), 403
    orders = Order.query.order_by(Order.created_at.desc()).all()
    res = []
    for o in orders:
        user = User.query.get(o.user_id)
        items = OrderItem.query.filter_by(order_id=o.id).all()
        items_res = []
        for i in items:
            p = Product.query.get(i.product_id)
            items_res.append({"product_name": p.item_name if p else "Deleted", "quantity": i.quantity, "price": i.price})
        res.append({
            "id": o.id,
            "user": user.fullname if user else "Unknown",
            "email": user.email if user else "",
            "total_amount": o.total_amount,
            "status": o.status, "delivery_address": o.delivery_address,
            "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "items": items_res
        })
    return jsonify({"success": True, "orders": res})

@app.route("/api/admin/orders/<int:order_id>/status", methods=["POST"])
@login_required
def update_order_status(order_id):
    if get_logged_in_user().userid != "admin@agrimitra": return jsonify({"success": False}), 403
    o = Order.query.get_or_404(order_id)
    o.status = request.json.get("status", o.status)
    db.session.commit()
    return jsonify({"success": True})

@app.route("/api/admin/users", methods=["GET"])
@login_required
def get_users():
    if get_logged_in_user().userid != "admin@agrimitra": return jsonify({"success": False}), 403
    users = User.query.all()
    res = [{"id": u.id, "fullname": u.fullname, "userid": u.userid, "email": u.email, "phone": u.phone} for u in users]
    return jsonify({"success": True, "users": res})

@app.route("/api/checkout", methods=["POST"])
@login_required
def checkout():
    user = get_logged_in_user()
    data = request.get_json(silent=True) or {}
    cart = data.get("cart", [])
    address = data.get("address", "")
    if not cart: return jsonify({"success": False, "message": "Cart is empty"}), 400
    
    total = 0
    order = Order(user_id=user.id, total_amount=0, status='Pending', delivery_address=address)
    db.session.add(order)
    db.session.flush() # get ID
    
    for item in cart:
        # Expected item: {product_id, quantity, price}
        p = Product.query.get(item.get("product_id"))
        if p:
            qty = float(item.get("quantity", 1))
            if p.stock < qty: return jsonify({"success": False, "message": f"Not enough stock for {p.item_name}"}), 400
            p.stock -= qty
            price = float(item.get("price", p.price))
            total += price * qty
            oi = OrderItem(order_id=order.id, product_id=p.id, quantity=qty, price=price)
            db.session.add(oi)
    
    order.total_amount = total
    db.session.commit()
    return jsonify({"success": True, "message": "Order placed successfully!"})


@app.route("/my-orders")
@login_required
def my_orders_page():
    user = get_logged_in_user()
    return render_template("orders.html", user=user, language=current_language(user), active_page="orders")

@app.route("/api/my-orders", methods=["GET"])
@login_required
def api_my_orders():
    user = get_logged_in_user()
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    res = []
    for o in orders:
        items = OrderItem.query.filter_by(order_id=o.id).all()
        items_res = []
        for i in items:
            p = Product.query.get(i.product_id)
            items_res.append({"name": p.item_name if p else "Deleted", "quantity": i.quantity, "price": i.price})
        res.append({
            "id": o.id,
            "total_amount": o.total_amount,
            "status": o.status, "delivery_address": o.delivery_address,
            "delivery_address": o.delivery_address,
            "created_at": o.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "items": items_res
        })
    return jsonify({"success": True, "orders": res})

@app.route("/api/orders/<int:order_id>/location", methods=["POST"])
@login_required
def provide_location(order_id):
    user = get_logged_in_user()
    o = Order.query.get_or_404(order_id)
    if o.user_id != user.id:
        return jsonify({"success": False}), 403
    address = request.json.get("address")
    if not address:
        return jsonify({"success": False, "message": "Address is required"}), 400
    
    o.delivery_address = address
    o.status = "Location Provided"
    db.session.commit()
    return jsonify({"success": True})

if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
