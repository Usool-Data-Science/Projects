document.addEventListener('DOMContentLoaded', function () {
    var formSwitch = document.querySelector("#formSwitch");
    var formContent = document.querySelector(".form--content");

    formSwitch.addEventListener('click', function () {
        if (formContent.classList.contains('hidden')) {
            formContent.classList.remove('hidden');
        } else {
            formContent.classList.add('hidden');
        }
    });
});