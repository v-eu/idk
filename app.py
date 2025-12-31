
from flask import Flask, request, render_template_string
import uuid, random, os

app = Flask(__name__)
os.makedirs("messages", exist_ok=True)

NEW_YEAR_MESSAGES = [
    "كل عام وأنت بخير 🎉 نتمنى لك سنة 2026 مليئة بالأمل وتحقيق الأحلام.",
    "مع بداية عام 2026 ✨ نتمنى لك أيامًا أجمل وسعادة دائمة.",
    "سنة جديدة تعني فرصة جديدة 🤍 كل عام وأنت بخير.",
    "2026 سنة الأمل 🌟 نتمنى لك راحة بال وفرح لا ينتهي.",
    "كل عام وأنت أقرب لأحلامك 🎊 سنة 2026 مباركة."
]

HOME_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>تهنئة 2026</title>
<style>
body {
    background:#050505;
    color:white;
    font-family:Arial;
    margin:0;
}
.container {
    max-width:420px;
    margin:auto;
    padding:20px;
}
.card {
    background:#0f0f0f;
    border-radius:16px;
    padding:20px;
}
h1 {
    text-align:center;
    color:#3f51b5;
}
p {
    text-align:center;
    color:#ccc;
    font-size:14px;
}
textarea {
    width:100%;
    height:120px;
    border-radius:10px;
    border:none;
    padding:12px;
    font-size:14px;
}
button {
    width:100%;
    margin-top:10px;
    padding:14px;
    border:none;
    border-radius:10px;
    background:#3f51b5;
    color:white;
    font-size:15px;
}
.link {
    background:black;
    margin-top:10px;
    padding:10px;
    border-radius:8px;
    word-break:break-all;
    font-size:13px;
}
.footer {
    text-align:center;
    margin-top:15px;
    color:#777;
    font-size:13px;
}
</style>
</head>
<body>
<div class="container">
<div class="card">

<h1>🎉 تهنئة السنة الجديدة 2026 🎉</h1>
<p>اكتب رسالة أو اطلب رسالة عشوائية، ثم انسخ الرابط وشاركه.</p>

<form method="post">
<textarea name="message">{{message}}</textarea>

<button name="action" value="random">🎁 رسالة تهنئة عشوائية</button>
<button name="action" value="create">🔗 إنشاء الرابط</button>
</form>

{% if link %}
<div class="link">{{link}}</div>
{% endif %}

<div class="footer">🤍 نتمنى لك سنة 2026 مليئة بالأمل 🤍</div>

</div>
</div>
</body>
</html>
"""

VIEW_HTML = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>رسالة تهنئة</title>
<style>
body {
    background:#050505;
    color:white;
    display:flex;
    align-items:center;
    justify-content:center;
    height:100vh;
    margin:0;
    font-family:Arial;
}
.box {
    background:#0f0f0f;
    padding:25px;
    border-radius:16px;
    max-width:420px;
    text-align:center;
}
</style>
</head>
<body>
<div class="box">
{{message}}
</div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    message = ""
    link = None

    if request.method == "POST":
        action = request.form["action"]

        if action == "random":
            message = random.choice(NEW_YEAR_MESSAGES)

        if action == "create":
            message = request.form["message"].strip()
            if message:
                mid = str(uuid.uuid4())[:6]
                with open(f"messages/{mid}.txt", "w", encoding="utf-8") as f:
                    f.write(message)
                link = request.host_url + "m/" + mid

    return render_template_string(HOME_HTML, message=message, link=link)

@app.route("/m/<mid>")
def view(mid):
    path = f"messages/{mid}.txt"
    if not os.path.exists(path):
        return "الرسالة غير موجودة"
    with open(path, encoding="utf-8") as f:
        msg = f.read()
    return render_template_string(VIEW_HTML, message=msg)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
