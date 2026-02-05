# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class StudentApplicationController(http.Controller):
    """Controller class to handle HTTP routes."""
    @http.route('/student-application', auth='public', website=True)
    def index(self, **kw):
        print("in student_application")
        current_academic_year=request.env["vm.academic.year"].sudo().search([("admission_open","=",True)], limit=1)
        if not current_academic_year:
            return "No Academic Year Open for Application"
                # request.render("student_application.index", {})
        else:
            grades=request.env["vm.student.grade"].sudo().search([("open_for_admission","=",True)])
            parent_relationships=request.env["vm.parent.relationship"].sudo().search([])
            company_id=request.env["res.company"].sudo().search([])
            nationalities=request.env["res.country"].sudo().search([])
            default_nationality=nationalities.filtered(lambda n:n.code=="EG")
        vals={
            "grades":grades,
            "parent_relationships":parent_relationships,
            "year":current_academic_year,
            "company_id":company_id,
            "nationalities":nationalities,
            "default_nationality":default_nationality
        }
        print("vals",vals)
        return request.render('virgin_mary_school.vm_student_application', vals)