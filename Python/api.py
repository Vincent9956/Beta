import os

from flask import Flask, request

app = Flask(__name__)

# Hardcoded secret key (security issue)
app.config["SECRET_KEY"] = "hardcoded-secret-key"  # ⚠️ Hardcoded secret key

IMAGE_TAG = os.environ.get("IMAGE_TAG", "unknown")


@app.route("/")
def index():
    # Using eval on user input (Remote Code Execution risk)
    user_input = request.args.get("tag", "default")
    result = eval(f'"{IMAGE_TAG}-{user_input}"')  # ⚠️ Dangerous usage
    return f"IMAGE_TAG: {result}"


if __name__ == "__main__":
    # Starting with debug mode enabled (should not be used in production)
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port, debug=True)  # ⚠️ Debug mode on
