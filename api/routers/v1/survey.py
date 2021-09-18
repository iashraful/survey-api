import uuid
from api.models.survey import SurveySection
from typing import List

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request

from api.core.auth import get_current_user
from api.core.database import get_db
from api.enums.survey_enums import QuestionTypeEnum
from api.models import QuestionOption, Survey, SurveyQuestion, User
from api.schemas.v1.survey import SurveyCreateSchema, SurveyDetailsSchema, SurveyQuestionSchema, SurveySchema, SurveyUpdateSchema

router = APIRouter()


@router.get('/surveys/', response_model=List[SurveySchema])
def get_surveys(db: Session = Depends(get_db), c_user: User = Depends(get_current_user)):
    surveys = Survey.objects(session=db).filter_by(
        user_id=c_user.id).order_by(Survey.published_time.desc()).all()
    return surveys


@router.get('/surveys/{survey_slug}/', response_model=SurveyDetailsSchema)
def get_survey_details(survey_slug: str, db: Session = Depends(get_db), c_user: User = Depends(get_current_user)):
    survey_details = Survey.objects(db).filter_by(slug=survey_slug).first()
    return survey_details


@router.get('/questions/{survey_id}/', response_model=List[SurveyQuestionSchema])
def get_questions(survey_id: int, db: Session = Depends(get_db), c_user: User = Depends(get_current_user)):
    """
    Get Questions for a specific survey
    :param survey_id: This is survey ID
    :param db: This is a session instance to access the database gently
    :return: Sqlalchemy queryset of objects
    """
    questions = SurveyQuestion.objects(db).filter_by(survey_id=survey_id).all()
    return questions


@router.post('/surveys/', response_model=SurveyDetailsSchema, status_code=201)
def create_survey(survey: SurveyCreateSchema, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    _survey = Survey(
        user_id=current_user.id, name=survey.name, instructions=survey.instructions,
        status=survey.status, slug=uuid.uuid4().hex
    )
    db.add(_survey)
    db.commit()
    _ques_option_list = []
    for section in survey.sections:
        _sec = SurveySection(name=section.name, survey_id=_survey.id)
        db.add(_sec)
        db.commit()

        for question in section.questions:
            if question.type not in QuestionTypeEnum.list_of_values():
                raise HTTPException(
                    status_code=400,
                    detail='Question Type doesn\'t found.'
                )
            _ques = SurveyQuestion(
                text=question.text, text_translation=question.text_translation,
                type=question.type, survey_id=_survey.id, section_id=_sec.id,
                status=question.status, is_required=question.is_required
            )
            db.add(_ques)
            db.commit()
            for opt in question.options:
                _ques_option_list.append(QuestionOption(
                    name=opt.name, name_translation=opt.name_translation,
                    question_id=_ques.id
                ))
    db.bulk_save_objects(_ques_option_list)
    db.commit()
    db.refresh(_survey)
    return _survey


@router.put('/surveys/{survey_slug}/', response_model=SurveyDetailsSchema, status_code=200)
def update_survey(survey_slug: str, survey: SurveyUpdateSchema, db: Session = Depends(get_db),
                  current_user: User = Depends(get_current_user)):
    _survey = Survey.objects(db).filter_by(slug=survey_slug).first()
    if not _survey:
        raise HTTPException(status_code=404, detail='No survey found.')
    _survey.user_id = current_user.id
    _survey.name = survey.name
    _survey.instructions = survey.instructions
    db.commit()
    _ques_option_list = []
    for section in survey.sections:
        _sec = SurveySection.objects(db).get(ident=section.id)
        _sec.name = section.name
        _sec.survey_id = _survey.id
        db.commit()

        for question in section.questions:
            if question.type not in QuestionTypeEnum.list_of_values():
                raise HTTPException(
                    status_code=400,
                    detail='Question Type doesn\'t found.'
                )
            _ques = SurveyQuestion.objects(db).get(ident=question.id)

            _ques.text = question.text
            _ques.text_translation = question.text_translation,
            _ques.type = question.type
            _ques.survey_id = _survey.id
            _ques.section_id = _sec.id
            _ques.status = question.status
            _ques.is_required = question.is_required
            db.commit()
            for opt in question.options:
                _opt = QuestionOption.objects(db).get(ident=opt.id)
                _opt.name = opt.name
                _opt.name_translation = opt.name_translation
                _opt.question_id = _ques.id
                db.commit()
    db.refresh(_survey)
    return _survey
