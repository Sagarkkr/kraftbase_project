from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from uuid import uuid4
from src.db import get_db
from src.apps.forms.schemas import Form, FormCreate, Submission, SubmissionListResponse, SubmissionResponse

router = APIRouter()

@router.post("/forms/create")
def create_form(form: FormCreate, db: Session = Depends(get_db)):
    new_form = Form(
        id=uuid4(),
        title=form.title,
        description=form.description,
        fields=[field.dict() for field in form.fields]
    )
    db.add(new_form)
    db.commit()
    db.refresh(new_form)
    return {"id": new_form.id, "message": "Form created successfully"}

@router.get("/forms/submissions/{form_id}", response_model=SubmissionListResponse)
def get_form_submissions(
    form_id: str,
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * limit
    total_count = db.query(func.count(Submission.id)).filter(Submission.form_id == form_id).scalar()
    submissions = (
        db.query(Submission)
        .filter(Submission.form_id == form_id)
        .offset(offset)
        .limit(limit)
        .all()
    )
    return SubmissionListResponse(
        total_count=total_count,
        page=page,
        limit=limit,
        submissions=[
            SubmissionResponse(
                submission_id=sub.id,
                submitted_at=sub.submitted_at.isoformat(),
                data=sub.data
            )
            for sub in submissions
        ]
    )

@router.post("/forms/submit/{form_id}")
def submit_form(
    form_id: str,
    responses: dict,
    db: Session = Depends(get_db)
):
    # Validate the form exists
    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Form not found",
        )

    # Validate each response against the form fields
    field_definitions = {field["field_id"]: field for field in form.fields}
    for response in responses["responses"]:
        field_id = response["field_id"]
        value = response["value"]

        if field_id not in field_definitions:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Invalid field_id: {field_id}",
            )

        field_type = field_definitions[field_id]["type"]
        if field_type == "string" and not isinstance(value, str):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Expected string value for field {field_id}",
            )
        elif field_type == "number" and not isinstance(value, (int, float)):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Expected numeric value for field {field_id}",
            )
        elif field_type == "boolean" and not isinstance(value, bool):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Expected boolean value for field {field_id}",
            )

    # Store submission in the database
    new_submission = Submission(
        id=uuid4(),
        form_id=form_id,
        data=responses,
    )
    db.add(new_submission)
    db.commit()
    db.refresh(new_submission)

    return {
        "submission_id": new_submission.id,
        "message": "Form submitted successfully"
    }

# Create Form
@router.post("/forms/create")
def create_form(form: FormCreate, db: Session = Depends(get_db)):
    new_form = Form(
        id=uuid4(),
        title=form.title,
        description=form.description,
        fields=[field.dict() for field in form.fields]
    )
    db.add(new_form)
    db.commit()
    db.refresh(new_form)
    return {"id": new_form.id, "message": "Form created successfully"}

# Delete Form
@router.delete("/forms/delete/{form_id}")
def delete_form(form_id: str, db: Session = Depends(get_db)):
    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise HTTPException(
            status_code=404,
            detail="Form not found"
        )
    db.delete(form)
    db.commit()
    return {"message": "Form deleted successfully"}

# Get All Forms
@router.get("/forms/")
def get_all_forms(db: Session = Depends(get_db)):
    forms = db.query(Form).all()
    return [
        {
            "id": form.id,
            "title": form.title,
            "description": form.description,
            "fields": form.fields,
        }
        for form in forms
    ]

# Get Single Form
@router.get("/forms/{form_id}")
def get_single_form(form_id: str, db: Session = Depends(get_db)):
    form = db.query(Form).filter(Form.id == form_id).first()
    if not form:
        raise HTTPException(
            status_code=404,
            detail="Form not found"
        )
    return {
        "id": form.id,
        "title": form.title,
        "description": form.description,
        "fields": form.fields,
    }
