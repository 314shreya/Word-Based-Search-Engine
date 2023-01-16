from flask import Blueprint, request, redirect, url_for, render_template
from app.constants.global_constants import GC
import spacy
from app.services.app_service import AppService
from app.services.response_service import ResponseService
import json


search_blueprint = Blueprint('search', __name__, template_folder="templates")


@search_blueprint.route('/', methods=['GET', 'POST'])
def home():
    if request.method == 'GET':

        response = {"files": {}, "searchResults": {}}

        return render_template("search.html", response=json.dumps(response))
    else:

        print("REQUEST", request.data)
        requestObject = request.data.decode("utf-8")

        requestWord = json.loads(requestObject).get('search', None)

        if not requestWord:
            response = ResponseService().create_empty_response()

            return response

        print("REQUESTING FOR", requestWord)

        lemmatizedObject = GC.SPACYLEMMATIZER(requestWord)

        searchWord = lemmatizedObject[0].lemma_

        print("SEARCHING FOR", searchWord)

        response = AppService().searchWord(searchWord)

        return json.dumps(response)
