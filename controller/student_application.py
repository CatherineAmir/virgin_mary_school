# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
import logging
_logger = logging.getLogger(__name__)


class StudentApplicationController(http.Controller):
    """Controller class to handle HTTP routes."""

    @http.route('/student-application', auth='public', website=True)
    def index(self, **kw):
        print("in student_application")
        current_academic_year = request.env["vm.academic.year"].sudo().search([("admission_open", "=", True)], limit=1)
        if not current_academic_year:
            return "No Academic Year Open for Application"
            # request.render("student_application.index", {})
        else:
            grades = request.env["vm.student.grade"].sudo().search([("open_for_admission", "=", True)])
            parent_relationships = request.env["vm.parent.relationship"].sudo().search([])
            company_id = request.env["res.company"].sudo().search([])
            nationalities = request.env["res.country"].sudo().search([])
            default_nationality = nationalities.filtered(lambda n: n.code == "EG")
            all_national_ids = request.env['vm.student'].sudo().search_read(domain=[], fields=['national_id'], offset=0,
                                                                            limit=None, order=None)
            print("all_national_ids", all_national_ids)
        vals = {
            "grades": grades,
            "parent_relationships": parent_relationships,
            "year": current_academic_year,
            "company_id": company_id,
            "nationalities": nationalities,
            "default_nationality": default_nationality,
            "all_national_ids": all_national_ids,
            "max_year": current_academic_year.date_required_for_application.year,
        }
        print("vals", vals)
        return request.render('virgin_mary_school.vm_student_application', vals)

    @http.route('/parent_detail/id/<string:national_id>', auth='public', website=True)
    def CreateStudent(self, **kw):
        print("in student_application", kw)
        national_id = kw.get('national_id', False)
        if not national_id:
            # todo
            return "No National ID for Application"
        STudentObJ=request.env["vm.student"].sudo()
        existance_student = STudentObJ.search([("national_id", '=', national_id)], limit=1)
        current_academic_year = request.env["vm.academic.year"].sudo().search([("admission_open", "=", True)], limit=1)
        print("existance_student",existance_student)
        if not existance_student:
            date_of_birth = kw.get('date_of_birth',False)
            if date_of_birth:
            # "Create new Student"
                vals = {
                "name_arabic": kw.get('student_name_arabic', ""),
                "name": kw.get('student_name_english', ""),
                "birth_date": datetime.strptime(date_of_birth, "%d/%m/%Y").date(),
                "place_of_birth": kw.get('place_of_birth', ""),
                "nationality":int(kw.get('nationality', 65)),
                "detailed_address": kw.get('detailed_address', ""),
                "national_id": kw.get('national_id', False),
                "grade_id": int(kw.get('grade_applied', 0)),
                "gender":kw.get('gender', "male"),
                "religion":kw.get('religion', "christian"),
                "transportation":kw.get('transportation', "bus"),
                "previous_school_name":kw.get("previous_school_name",""),
                "number_of_brothers":int(kw.get('number_of_brothers', 0)),
                "number_of_sisters":int(kw.get('number_of_sisters', 0)),
                "parent_marital_status":kw.get('marital_status', "married"),
                "legal_custodian":kw.get('legal_custodian', "father"),
                "current_academic_year":current_academic_year.id,

            }
                print("vals", vals)
                try:
                    student_id=STudentObJ.create(vals)
                except Exception as e:
                    _logger.error(f"Application Error for National ID: {national_id} Error is {e}")

                else:
                    return self.get_parent_data(kw,student_id,national_id)



        elif not existance_student.parent_ids:
            return self.get_parent_data(kw, existance_student, national_id)
        else:
            # todo
            return "Thank YOu"







    def get_parent_data(self,kw,student_id,national_id):
        siblings = int(kw.get('number_of_brothers', 0)) + int(kw.get('number_of_sisters', 0))
        parent_grades = request.env['vm.student.grade'].sudo().search([("is_parent", "=", True)])
        nationalities = request.env["res.country"].sudo().search([])
        default_nationality = nationalities.filtered(lambda n: n.code == "EG")
        all_national_ids = request.env['vm.parent'].sudo().search_read(domain=[], fields=['national_id'], offset=0,
                                                                       limit=None, order=None)
        vals = {
            "student_id": student_id,
            "siblings": siblings,
            "national_id": national_id,
            "nationalities": nationalities,
            "parent_grades": parent_grades,
            "default_nationality": default_nationality,
            "all_national_ids": all_national_ids,
        }

        return request.render("virgin_mary_school.parent_data", vals)

    @http.route('/thank_you',auth='public', website=True)
    def thank_you(self,**kw):
        print("Thank You",kw)
        #     todo


        return request.render("virgin_mary_school.application_thank_you")
