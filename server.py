import os
from flask import Flask, request, render_template, flash, redirect, url_for
from werkzeug.utils import secure_filename
app=Flask('')
app.config["SECRET_KEY"] = "supersecretkey"
from werkzeug.utils import secure_filename
UPLOAD_FOLDER = "uploads"  # Папка для сохранения файлов
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # Создаём папку, если её нет

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            flash("Файл не найден!", "danger")
            return redirect(url_for("index"))

        file = request.files["file"]
        if file.filename == "":
            flash("Выберите файл перед загрузкой!", "warning")
            return redirect(url_for("index"))

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)

        try:
            # Пробуем читать как текст
            file.seek(0)
            file.save(filepath)
        except UnicodeDecodeError:
            # Если не текстовый, сохраняем как бинарный
            file.seek(0)  # Возвращаем указатель в начало файла
            file.save(filepath)
            flash(f"Бинарный файл '{filename}' сохранён!", "primary")

        return redirect(url_for("index"))

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
