from flask import Blueprint, render_template, abort, request, redirect, url_for, flash
from flask_login import login_required, current_user
from sqlalchemy import text

from app import db
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
    # search can be done by similarity or keywords search
    # check if the parameter is similarity or keywords
    if request.form.get("searchOption") == "similarity":
        query = request.form.get("search")
        ai_results = ai_utils.search_documents(ai_utils.embeddings, query)

        # Get the documents from the database
        results = []

        # make sure that the results are in order of similarity
        # similarity must be bigger than 0.2
        for result in ai_results:
            if result[1] > 0.2:
                document = Document.query.get(result[0])
                if document:
                    results.append(document)

        return render_template("home.html", documents=results)

    elif request.form.get("searchOption") == "keywords":
        query = request.form.get("search")

        # Get the query and extract the keywords
        keywords = ai_utils.extract_keywords(ai_utils.nlp, query)

        # Filter the documents by keywords
        try:
            sql_query = "content LIKE '%" + "%' OR content LIKE '%".join(keywords) + "%'"
            results = Document.query.filter(text(sql_query)).all()
        except:
            flash("Database fetch error.", "danger")
            return render_template("home.html")

        return render_template("home.html", documents=results if len(keywords) > 0 else [])

    flash("Invalid search query.", "danger")
    return render_template("home.html")


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
