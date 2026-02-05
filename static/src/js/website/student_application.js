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