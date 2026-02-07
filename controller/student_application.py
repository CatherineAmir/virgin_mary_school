# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
from datetime import datetime
import logging
import pybase64
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
                "detailed_address": kw.get('address', ""),
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

            else:
                return request.redirect("/student-application")



        elif not existance_student.parent_ids:
            return self.get_parent_data(kw, existance_student, national_id)
        else:
            # todo
            return request.redirect("/thank_you")







    def get_parent_data(self,kw,student_id,national_id):

        parent_grades = request.env['vm.student.grade'].sudo().search([("is_parent", "=", True)])
        nationalities = request.env["res.country"].sudo().search([])
        default_nationality = nationalities.filtered(lambda n: n.code == "EG")
        all_national_ids = request.env['vm.parent'].sudo().search_read(domain=[], fields=['national_id'], offset=0,
                                                                         limit=None, order=None)

        parent_relation=request.env['vm.parent.relationship'].sudo().search([])
        siblings=student_id.number_of_brothers+student_id.number_of_sisters
        current_academic_year = request.env["vm.academic.year"].sudo().search([("admission_open", "=", True)], limit=1)
        vals = {
            "student_id": student_id,
            "siblings": siblings,
            "national_id": national_id,
            "nationalities": nationalities,
            "parent_grades": parent_grades,
            "default_nationality": default_nationality,
            "all_national_ids": all_national_ids,
            "year":current_academic_year,
            "parent_relation":parent_relation,
            "father_default":1,
            "mother_default":2,
        }

        return request.render("virgin_mary_school.parent_data", vals)

    @http.route('/thank_you',auth='public', website=True,methods=["GET","POST"])
    def thank_you(self,**kw):
        print("Thank You",kw)
        national_id = kw.get("national_id", False)
        if not national_id:
            return request.redirect("/student-application")

        else:
            student_id=request.env['vm.student'].sudo().search([("national_id", "=", national_id)],limit=1)
            if not student_id:
                return request.redirect("/student-application")


        vals=[
            {
            "name":kw.get("father_name",""),
            "country_id":int(kw.get("father_nationality",0)),
            "national_id":kw.get("national_id_father",0),
            "mobile":kw.get("father_phone",""),
            "email":kw.get("father_email",""),
            "address":kw.get("father_address",""),
            "job":kw.get("father_job",""),
            "education":kw.get("father_education",""),
            "relationship_id":int(kw.get("father_parent_relation",1)),
            "student_ids": [(6, 0, [student_id.id])]

        },
            {
            "name": kw.get("mother_name", ""),
            "country_id": int(kw.get("mother_nationality", 0)),
            "national_id": kw.get("mother_national_id", 0),
            "mobile": kw.get("mother_phone", ""),
            "email": kw.get("mother_email", ""),
            "address": kw.get("mother_address", ""),
            "job": kw.get("mother_job", ""),
            "education": kw.get("mother_education", ""),
            "relationship_id": int(kw.get("mother_parent_relation",2)),
            "student_ids":[(6,0,[student_id.id])]

        }

        ]
        # print("vals",vals)
        try:
            parents=request.env['vm.parent'].sudo().create(vals)
            # print("parents",parents)
            father=parents[0]
            mother=parents[1]
        except Exception as e:
            _logger.error(f"Student with national id: {national_id} Error is {e} in parent Form")

        else:
            siblings=[key for key,value in kw.items() if key.startswith("sibling")]
            sibling_data=[]
            total_siblings=int(len(siblings)/2)
            for s in range(0,total_siblings):
                sibling_data.append({
                    "name":kw.get(f"sibling_name_{s}",""),
                    "grade_id":int(kw.get(f"sibling_grade_{s}",0)),
                    "student_id":student_id.id,
                })


            request.env['vm.siblings'].sudo().create(sibling_data)

            Attachments = request.env['ir.attachment'].sudo()
            files=[]
            docs=[key  for key,value in kw.items() if key.endswith('_docs')]
            if len(docs):
                for doc in docs:
                    name = kw.get(doc).filename
                    file = kw.get(doc)

                    if 'father' in doc:

                        files.append({
                            'name': name,
                            'res_name': name,
                            'type': 'binary',
                            'res_model': "vm.parent",
                            'res_id': father.id ,
                            'datas': pybase64.b64encode(file.read()),

                        })
                    elif 'mother' in doc:
                        files.append({
                            'name': name,
                            'res_name': name,
                            'type': 'binary',
                            'res_model': "vm.parent",
                            'res_id': mother.id,
                            'datas': pybase64.b64encode(file.read()),

                        })
                    else:
                        if "image" in doc:
                            student_id.image_1920 = pybase64.b64encode(file.read())
                        else:
                            files.append({
                                'name': name,
                                'res_name': name,
                                'type': 'binary',
                                'res_model': "vm.student",
                                'res_id': student_id.id,
                                'datas': pybase64.b64encode(file.read()),

                            })


            attachment_ids=Attachments.create(files)
            print(attachment_ids)







        #     todo siblings docs
        # todo garedien level
        # validation natioanl id function cause error
        # email raise ValidationError(_('Validation error message'))
        # invalid text (residence)



        return request.render("virgin_mary_school.application_thank_you")
