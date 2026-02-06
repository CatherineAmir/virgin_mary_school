document.addEventListener('DOMContentLoaded', function () {
    const forms = document.querySelectorAll('.needs-validation');
    // console.log("DOMContentLoaded", forms);

    Array.from(forms).forEach(form => {
        form.addEventListener('submit', function (e) {
            // console.log("e in form Validation", e)
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });
});
window.showDatePicker = function (dateInput) {

    if (typeof flatpickr === 'undefined') {
        console.warn("Flatpickr not yet ready — retrying...");

    }
    const maxYear = document.querySelector("#date_of_birth").getAttribute("data-year");
    console.log("maxYear", maxYear);
    let input = document.getElementById("date_of_birth");
    console.log("input", input)
    maxDate=new Date(new Date(maxYear,9,1).setFullYear(new Date().getFullYear() - 4)),
    console.log("maxDate", maxDate)
        flatpickr(dateInput, {

        dateFormat: "d/m/Y",
        maxDate: maxDate,
        altInput: false,
        onChange: function (selectedDate, dateStr, instance) {

            if (selectedDate.length === 1) {


                input.value = dateStr;

                instance.close(); // Close calendar after selection
            }
        }


    }).open()

}



function onchangeNameArabic(input) {
    console.log("onchangeNameArabic", input);
    let name_ok = /^[A-Za-z]+$/;

    const member_name = input.value;


    let space_counts = member_name.split(" ").length - 1

    let member_name_without_spaces = member_name.replace(/\s/g, '')
    new RegExp(name_ok).test(member_name_without_spaces);
    if (!(member_name_without_spaces && (space_counts >= 2))) {

        input.setCustomValidity("Arabic Name is missing !, should first_name middle_name last_name\" )!")


    } else {

        input.setCustomValidity("")


    }
    input.closest('form').classList.add('was-validated');
}

function onchangeNameEnglish(input) {

    let name_ok = /^[A-Za-z]+$/;

    const member_name = input.value;


    let space_counts = member_name.split(" ").length - 1

    let member_name_without_spaces = member_name.replace(/\s/g, '')
    new RegExp(name_ok).test(member_name_without_spaces);
    if (!(member_name_without_spaces && (space_counts >= 2))) {

        input.setCustomValidity("English Name is missing !, should first_name middle_name last_name\" )!")


    } else {

        input.setCustomValidity("")


    }
    input.closest('form').classList.add('was-validated');
}

// todo
// onchange national id
// onchange date
// october validation

function onChangeNationalId(nationalIdInput) {
    const id_v = /^\d{14}$/;
    // console.log("onChangeNationalId");
    let national_id = nationalIdInput.value.replaceAll(" ", "");
    const NationalIdInvalidDiv = document.getElementById("national_id_invalid_feedback");

    let nationality = document.getElementById("nationality")
    if (nationality) {
        nationality = nationality.value
    }


    console.log("nationality", nationality);
    const nationalIdArray = document.querySelector("#national_id").getAttribute("data");
    console.log("nationalIDArray", nationalIdArray);
    if(nationalIdArray) {

        let nationalIDArray = JSON.parse(nationalIdArray.replaceAll("'", '"').replaceAll("None", "")
            .replaceAll("+", "").replaceAll(" ", "").replaceAll("-", "").replaceAll(/\bNone\b/g, 'null').replaceAll(/\bFalse\b/g, 'false').replaceAll(/[\s\-+]/g, ''));
        console.log("nationalIDArray", nationalIDArray);


        let searchStudents = searchID(national_id.replaceAll("-", '"').replaceAll("+", "").replaceAll(" ", "").replaceAll(/\bNone\b/g, 'null').replaceAll(/\bFalse\b/g, 'false').replaceAll(/[\s\-+]/g, ''), nationalIDArray);
        if (searchStudents !== -1) {

            nationalIdInput.setCustomValidity("Your Mobile Is Registered before you can't fill a new form");
            NationalIdInvalidDiv.textContent = "Your National Id Is Registered before you can't fill a new form";


        }
    }

    if (nationality && nationality === (65).toString()) {
        console.log("Egyptian National ID Validation");
        console.log("national_id", national_id.length);
        console.log("national_idstart", national_id[0]);
        if (!((national_id.match(id_v)) && national_id.startsWith("3"))) {
            // console.log("E", "Failed");
            nationalIdInput.setCustomValidity("National ID Format is incorrect! It should be 14 digits starting 3");


        } else {
            nationalIdInput.setCustomValidity("");


        }
    } else {

        nationalIdInput.setCustomValidity("");


    }
    console.log("national_id",national_id)
    $('form').attr('action', '/parent_detail/id/' + national_id.replaceAll(" ", ""));
    nationalIdInput.closest('form').classList.add('was-validated');
}

function onchangeImage(e) {
    document.getElementById('customerImage').addEventListener('change', function (e) {
        const files = e.target.files;
        const previewContainer = document.getElementById('imagePreviewContainer');
        previewContainer.innerHTML = ''; // Clear previous previews

        if (files.length > 0) {
            for (let i = 0; i < files.length; i++) {
                const file = files[i];

                if (file.type.startsWith('image/')) {
                    const reader = new FileReader();

                    reader.onload = function (event) {
                        const imgWrapper = document.createElement('div');
                        imgWrapper.className = 'mb-2';
                        imgWrapper.innerHTML = `
                                <div class="card">
                                    <div class="card-body">
                                        <p class="mb-2"><strong>${file.name}</strong> (${(file.size / 1024).toFixed(2)} KB)</p>
                                        <img src="${event.target.result}" class="img-fluid img-thumbnail" alt="Preview" style="max-height: 200px;">
                                    </div>
                                </div>
                            `;
                        previewContainer.appendChild(imgWrapper);
                    };

                    reader.readAsDataURL(file);
                }
            }
        }
    });
}

// Form submission


// <input type="file"> with accept="image/*" to only allow image files
//     multiple attribute to allow multiple image uploads
//     Image preview - Shows thumbnails of selected images before submission
//     File info display - Shows filename and file size
//     FormData handling for proper file upload
//
//     Options you can customize:
//
//     Remove multiple if you only want single image upload
//     Change accept="image/*" to accept="image/jpeg,image/png" for specific formats
//     Add required attribute if image upload is mandatory
//
//     Would you like me to modify anything about the image upload functionality?
//     }


function onChangeNationalIdParent(nationalIdInput) {
    const id_v = /^\d{14}$/;
    // console.log("onChangeNationalId");
    let national_id = nationalIdInput.value.replaceAll(" ", "");
    const NationalIdInvalidDiv = document.getElementById("national_id_invalid_feedback");

    let nationality = document.getElementById("nationality")
    if (nationality) {
        nationality = nationality.value
    }


    console.log("nationality", nationality);
    const nationalIdArray = document.querySelector("#national_id").getAttribute("data");
    console.log("nationalIDArray", nationalIdArray);
    if(nationalIdArray) {

        let nationalIDArray = JSON.parse(nationalIdArray.replaceAll("'", '"').replaceAll("None", "")
            .replaceAll("+", "").replaceAll(" ", "").replaceAll("-", "").replaceAll(/\bNone\b/g, 'null').replaceAll(/\bFalse\b/g, 'false').replaceAll(/[\s\-+]/g, ''));
        console.log("nationalIDArray", nationalIDArray);


        let searchparents = searchID(national_id.replaceAll("-", '"').replaceAll("+", "").replaceAll(" ", "").replaceAll(/\bNone\b/g, 'null').replaceAll(/\bFalse\b/g, 'false').replaceAll(/[\s\-+]/g, ''), nationalIDArray);
        if (searchStudents !== -1) {

            nationalIdInput.setCustomValidity("Your National Id Is Registered before you can't fill a new form");
            NationalIdInvalidDiv.textContent = "Your National Id Is Registered before you can't fill a new form";


        }
    }

    if (nationality && nationality === (65).toString()) {
        console.log("Egyptian National ID Validation");
        console.log("national_id", national_id.length);
        console.log("national_idstart", national_id[0]);
        if (!((national_id.match(id_v)) && (national_id.startsWith("3") || national_id.startsWith("2")))) {
            // console.log("E", "Failed");
            nationalIdInput.setCustomValidity("National ID Format is incorrect! It should be 14 digits starting 2 or 3");


        } else {
            nationalIdInput.setCustomValidity("");


        }
    } else {

        nationalIdInput.setCustomValidity("");


    }
    console.log("national_id",national_id)
    $('form').attr('action', '/parent_detail/id/' + national_id.replaceAll(" ", ""));
    nationalIdInput.closest('form').classList.add('was-validated');
}

function searchID(str, strArr) {
    if (strArr) {


        for (let i = 0; i < strArr.length; i++) {
            if (str === strArr[i]) {
                return i
            }

        }
        return -1
    } else {
        return -1
    }


}