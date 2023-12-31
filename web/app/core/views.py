from flask import Blueprint, render_template, abort, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from sqlalchemy import text

from app import app, db
from app.core.models import Document
from .forms import UploadForm
from app import ai_utils

core_bp = Blueprint("core", __name__)

@login_required
@core_bp.route("/home", methods=["GET"])
def home():
    # Get users last 3 documents
    documents = Document.query.filter_by(owner=current_user).order_by(
        Document.id.desc()).limit(3).all()

    return render_template("home.html", documents=documents)


@login_required
@core_bp.route("/search", methods=["POST"])
def search():
    # search can be done by keywords or by chatbot
    # check if the parameter is keywords or query
    if request.form.get("keywords"):
        keywords = request.form.get("keywords")
        ai_results = ai_utils.search_documents(ai_utils.embeddings, keywords)

        # Get the documents from the database
        results = Document.query.filter(Document.id.in_([result[0] for result in ai_results])).all()

        return jsonify({
            "response":None,
            "results": [result.to_dict() for result in results]
            })

    elif request.form.get("query"):
        query = request.form.get("query")

        # Get the query and extract the keywords (named entities) using NER
        sql_query = ai_utils.extract_keywords(ai_utils.nlp, query)
        results = db.engine.execute(text(sql_query % current_user)).fetchall()

        return jsonify({
            "response":"Here is what I found:",
            "results":[result.to_dict() for result in results]
            })
    
    return jsonify({"error": "Invalid query."}), 400



@login_required
@core_bp.route("/document/<int:document_id>")
def view(document_id):
    document = Document.query.get_or_404(document_id)

    # check if the document belongs to user
    if document.owner != current_user:
        abort(403)

    return render_template("view.html", document=document)


@login_required
@core_bp.route("/upload", methods=["GET", "POST"])
def upload():
    form = UploadForm(request.form)

    if form.validate_on_submit():
        document = Document(
            title=form.title.data,
            content=form.content.data,
            owner=current_user
        )
        db.session.add(document)
        db.session.commit()

        # Save document to txtai
        ai_utils.add_document(ai_utils.embeddings, document)

        flash("Successfully uploaded document!", "success")
        return redirect(url_for("core.view", document_id=document.id))

    return render_template("upload.html")


@login_required
@core_bp.route("/delete/<int:document_id>", methods=["POST"])
def delete(document_id):
    document = Document.query.get_or_404(document_id)

    # check if the document belongs to user
    if document.owner != current_user:
        abort(403)

    db.session.delete(document)
    db.session.commit()

    # delete from txtai as well
    ai_utils.delete_document(ai_utils.embeddings, document)

    flash("Successfully deleted document!", "success")
    return redirect(url_for("core.home"))
