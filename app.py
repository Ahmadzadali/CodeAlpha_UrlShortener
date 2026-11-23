from flask import Flask, jsonify, redirect, request
import database
import service

app = Flask(__name__)


# API Endpoint: Uzun URL-i qəbul edir və qısa kod yaradır
@app.route("/api/shorten", methods=["POST"])
def shorten():
  data = request.get_json(silent=True) or {}
  raw_url = data.get("url")

  try:
    result = service.create_short_url(
        raw_url=raw_url, base_url=request.host_url
    )
    return jsonify(result), 201
  except ValueError as e:
    return jsonify({"error": str(e)}), 400


# Redirect Route: Qısa URL-ə daxil olduqda orijinal URL-ə yönləndirir
@app.route("/<short_code>", methods=["GET"])
def redirect_to_original(short_code: str):
  original_url = service.resolve_short_url(short_code)
  if not original_url:
    return jsonify({"error": "Qısa URL tapılmadı."}), 404

  return redirect(original_url, code=302)


# Statistika Endpoint-i (Bonus: neçə dəfə klikləndiyini görmək üçün)
@app.route("/api/stats/<short_code>", methods=["GET"])
def stats(short_code: str):
  record = database.get_by_short_code(short_code)
  if not record:
    return jsonify({"error": "Qısa URL tapılmadı."}), 404

  return (
      jsonify({
          "short_code": record["short_code"],
          "original_url": record["original_url"],
          "clicks": record["clicks"],
          "created_at": record["created_at"],
      }),
      200,
  )


if __name__ == "__main__":
  database.init_db()
  app.run(debug=True, port=5000)