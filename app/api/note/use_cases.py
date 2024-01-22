import datetime
import math

from werkzeug.exceptions import HTTPException
from sqlalchemy import func, select
from db import get_session
from api.base.base_schemas import PaginationMetaResponse, PaginationParams
from models.note import Note, NoteSchema
from .schemas import CreateNoteRequest, UpdateNoteRequest

class CreateNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(
            self,
            user_id: int,
            request: CreateNoteRequest
        ) -> NoteSchema:
        with self.session as session:
            note = session.execute(
                select(Note).where(Note.created_by == user_id)
                )
            note = note.scalars().first()

            note = Note()
            note.title = request.title
            note.content = request.content
            note.created_at = datetime.datetime.utcnow()
            note.updated_at = datetime.datetime.utcnow()
            note.created_by = user_id
            note.updated_by = user_id

            session.add(note)
            session.flush()

            return NoteSchema.from_orm(note)

class ReadAllNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(
        self,
        user_id: int,
        page_params: PaginationParams,
        include_deleted: bool,
        filter_user: bool
    ) -> (list[dict], PaginationMetaResponse):
        with self.session as session:
            total_item = (
                select(func.count())
                .select_from(Note)
            )

            query = (
                select(Note)
                .offset((page_params.page - 1) * page_params.item_per_page)
                .limit(page_params.item_per_page)
            )

            if filter_user:
                total_item = total_item.filter(Note.created_by == user_id)
                query = query.filter(Note.created_by == user_id)

            if not include_deleted:
                total_item = total_item.filter(Note.deleted_at == None)
                query = query.filter(Note.deleted_at == None)

            total_item = session.execute(total_item)
            total_item = total_item.scalar()

            paginated_query = session.execute(query)
            paginated_query = paginated_query.scalars().all()

            note = [NoteSchema.from_orm(p).__dict__ for p in paginated_query]

            meta = PaginationMetaResponse(
                total_item=total_item,
                page=page_params.page,
                item_per_page=page_params.item_per_page,
                total_page=math.ceil(total_item / page_params.item_per_page),
            )

            return note, meta

class ReadNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(
            self,
            user_id: int,
            note_id: int
    ) -> NoteSchema:
        with self.session as session:
            note = session.execute(
                select(Note)
                .where((Note.created_by == user_id) &
                       (Note.note_id == note_id) &
                       (Note.deleted_at == None))
            )
            note = note.scalars().first()

            if not note:
                exception = HTTPException(description="note not found")
                exception.code = 404
                raise exception

            return NoteSchema.from_orm(note)

class UpdateNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(
            self,
            user_id: int,
            note_id: int,
            request: UpdateNoteRequest
    ) -> NoteSchema:
        with self.session as session:
            note = session.execute(
                select(Note)
                .where((Note.created_by == user_id) &
                       (Note.note_id == note_id) &
                       (Note.deleted_at == None))
            )
            note = note.scalars().first()

            if not note:
                exception = HTTPException(description="note not found")
                exception.code = 404
                raise exception

            note.title = request.new_title
            note.content = request.new_content
            note.updated_at = datetime.datetime.utcnow()
            note.updated_by = user_id

            session.flush()
            return NoteSchema.from_orm(note)

class DeleteNote:
    def __init__(self) -> None:
        self.session = get_session()

    def execute(
        self,
        user_id: int,
        note_id: int
    ) -> NoteSchema:
        with self.session as session:
            note = session.execute(
                select(Note)
                .where((Note.created_by == user_id) &
                    (Note.note_id == note_id) &
                    (Note.deleted_at == None))
            )
            note = note.scalars().first()

            if not note:
                exception = HTTPException(description="note not found")
                exception.code = 404
                raise exception

            note.deleted_at = datetime.datetime.utcnow()
            note.deleted_by = user_id

            session.flush()

            return NoteSchema.from_orm(note)
