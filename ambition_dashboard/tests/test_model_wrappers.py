from django.test import TestCase, tag
from edc_base.utils import get_utcnow
from edc_lab_dashboard.model_wrappers import RequisitionModelWrapper
from edc_model_wrapper.tests import ModelWrapperTestHelper

from ..model_wrappers import AppointmentModelWrapper
from ..model_wrappers import SubjectConsentModelWrapper
from ..model_wrappers import SubjectLocatorModelWrapper
from ..model_wrappers import SubjectVisitModelWrapper
from ..model_wrappers import SubjectScreeningModelWrapper
from .models import SubjectScreening, Appointment, SubjectVisit


class SubjectModelWrapperTestHelper(ModelWrapperTestHelper):
    dashboard_url = '/subject_dashboard/'


class ScreeningModelWrapperTestHelper(ModelWrapperTestHelper):
    dashboard_url = '/screening_listboard/'


class TestModelWrappers(TestCase):

    model_wrapper_helper_cls = SubjectModelWrapperTestHelper

    @tag('1')
    def test_subject_screening(self):
        helper = ScreeningModelWrapperTestHelper(
            model_wrapper=SubjectScreeningModelWrapper,
            app_label='ambition_dashboard',
            screening_identifier='ABCDEFGH')
        helper.test(self)

    @tag('1')
    def test_subject_consent(self):
        SubjectScreening.objects.create(
            screening_identifier='1234')
        helper = self.model_wrapper_helper_cls(
            model_wrapper=SubjectConsentModelWrapper,
            app_label='ambition_dashboard',
            subject_identifier='092-12345')
        helper.test(self)

    @tag('1')
    def test_subject_locator(self):
        helper = self.model_wrapper_helper_cls(
            model_wrapper=SubjectLocatorModelWrapper,
            app_label='ambition_dashboard',
            subject_identifier='092-12345')
        helper.test(self)

    def test_appointment(self):

        class MySubjectVisitModelWrapper(SubjectVisitModelWrapper):
            model = 'ambition_dashboard.subjectvisit'

        class MyAppointmentModelWrapper(AppointmentModelWrapper):
            visit_model_wrapper_cls = MySubjectVisitModelWrapper

        # note: AppointmentModelWrapper has no class attr model
        helper = self.model_wrapper_helper_cls(
            model_wrapper=MyAppointmentModelWrapper,
            app_label='edc_appointment',
            model='edc_appointment.appointment',
            appt_datetime=get_utcnow(),
            subject_identifier='092-12345')
        helper.test(self)

    def test_subject_visit(self):
        appointment = Appointment.objects.create(
            appt_datetime=get_utcnow(),
            subject_identifier='092-12345',)
        helper = self.model_wrapper_helper_cls(
            model_wrapper=SubjectVisitModelWrapper,
            app_label='ambition_dashboard',
            subject_identifier='092-12345',
            appointment=appointment)
        helper.test(self)

    def test_subject_requisition(self):
        class MyRequisitionModelWrapper(RequisitionModelWrapper):
            requisition_panel_name = 'vl'
        appointment = Appointment.objects.create(
            appt_datetime=get_utcnow(),
            subject_identifier='092-12345')
        subject_visit = SubjectVisit.objects.create(
            subject_identifier='092-12345',
            appointment=appointment)
        helper = self.model_wrapper_helper_cls(
            model_wrapper=MyRequisitionModelWrapper,
            app_label='ambition_dashboard',
            subject_visit=subject_visit)
        helper.test(self)
