from flask import Blueprint, jsonify, request
from werkzeug.exceptions import HTTPException
from flask_pydantic import validate
from api.base.base_schemas import BaseResponse
from middlewares.authentication import get_user_id_from_access_token
from .schemas import (
    CreateNoteRequest,
    CreateNoteResponse,
    ReadAllNoteParamRequest,
    ReadAllNoteResponse,
    ReadNoteResponse,
    UpdateNoteRequest,
    UpdateNoteResponse,
    DeleteNoteResponse
)
from .use_cases import CreateNote, ReadAllNote, ReadNote, UpdateNote, DeleteNote

router = Blueprint("note", __name__, url_prefix='/api/v1/notes')

@router.route("/", methods=["POST"])
@validate()
def create(
    body: CreateNoteRequest
) -> CreateNoteResponse:
    try:
        token_user_id = get_user_id_from_access_token(request)

        create_note = CreateNote()
        resp_data = create_note.execute(
            user_id=token_user_id,
            request=body
        )
        return jsonify(CreateNoteResponse(
            status="success",
            message="success create new note",
            data=resp_data.__dict__,
        ).__dict__), 200

    except HTTPException as ex:
        return jsonify(CreateNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code

    except Exception as e:
        message = "failed to create new note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(CreateNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500

@router.route("/", methods=["GET"])
@validate()
def read_all(
    query: ReadAllNoteParamRequest
):
    try:
        token_user_id = get_user_id_from_access_token(request)

        read_all_note = ReadAllNote()
        resp_data = read_all_note.execute(
            user_id=token_user_id,
            page_params=query,
            include_deleted=query.include_deleted,
            filter_user=query.filter_user
        )
        return jsonify(ReadAllNoteResponse(
            status="success",
            message="success read all note",
            data={"records":resp_data[0], "meta":resp_data[1].__dict__},
        ).__dict__), 200

    except HTTPException as ex:
        return jsonify(ReadAllNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code

    except Exception as e:
        message = "failed to read all note"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(ReadAllNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500

@router.route("/<note_id>", methods=["GET"])
@validate()
def read(
    note_id: int
):
    try:
        token_user_id = get_user_id_from_access_token(request)

        read_note = ReadNote()
        resp_data = read_note.execute(
            user_id=token_user_id,
            note_id=note_id,
        )
        return jsonify(ReadNoteResponse(
            status="success",
            message=f"success read note with id={note_id}",
            data=resp_data.__dict__,
        ).__dict__), 200

    except HTTPException as ex:
        return jsonify(ReadNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code

    except Exception as e:
        message = f"failed to read note with id={note_id}"
        if hasattr(e, "message"):
            message = e.message
        elif hasattr(e, "detail"):
            message = e.detail

        return jsonify(ReadNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500

@router.route("/<note_id>", methods=["PUT"])
@validate()
def update(
    note_id: int,
    body: UpdateNoteRequest
) -> UpdateNoteResponse:
    try:
        token_user_id = get_user_id_from_access_token(request)

        update_note = UpdateNote()
        resp_data = update_note.execute(
            user_id=token_user_id,
            note_id=note_id,
            request=body
        )
        return jsonify(UpdateNoteResponse(
            status="success",
            message=f"success update note with id={note_id}",
            data=resp_data.__dict__,
        ).__dict__), 200

    except HTTPException as ex:
        return jsonify(UpdateNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code

    except Exception as e:
        message=f"failed to update note with id={note_id}"
        if hasattr(e, 'message'):
            message = e.message
        elif hasattr(e, 'detail'):
            message = e.detail

        return jsonify(UpdateNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500

@router.route("/<note_id>", methods=["DELETE"])
def delete(
    note_id: int
):
    try:
        token_user_id = get_user_id_from_access_token(request)

        delete_note = DeleteNote()
        resp_data = delete_note.execute(
            user_id=token_user_id,
            note_id=note_id
        )
        return jsonify(DeleteNoteResponse(
            status="success",
            message=f"success delete note with id={note_id}",
            data=resp_data.__dict__,
        ).__dict__), 200

    except HTTPException as ex:
        return jsonify(DeleteNoteResponse(
            status="error",
            message=ex.description,
            data=None
        ).__dict__), ex.code

    except Exception as e:
        message=f"failed to delete note with id={note_id}"
        if hasattr(e, 'message'):
            message = e.message
        elif hasattr(e, 'detail'):
            message = e.detail

        return jsonify(DeleteNoteResponse(
            status="error",
            message=message,
            data=None
        ).__dict__), 500
