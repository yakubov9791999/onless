// get csrftoken from cookie
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(function () {
    $('.img-responsive').click(function (event) {
        var i_path = $(this).attr('src');

        $('body').append('<div id="overlay"></div><div id="magnify"><img src="' + i_path + '"><div id="close-popup"><i></i></div></div>');
        $('#magnify').css({
            left: ($(document).width() - $('#magnify').outerWidth()) / 4,
            // top: ($(document).height() - $('#magnify').outerHeight())/2 upd: 24.10.2016
            top: ($(window).height() - $('#magnify').outerHeight()) / 4
        });
        $('#overlay, #magnify').fadeIn('fast');
    });

    $('body').on('click', '#close-popup, #overlay', function (event) {
        event.preventDefault();
        $('#overlay, #magnify').fadeOut('fast', function () {
            $('#close-popup, #magnify, #overlay').remove();
        });
    });
});

function parseDate(value) {
    var date = value.split("-");
    var y = parseInt(date[0], 10),
        m = parseInt(date[1], 10),
        d = parseInt(date[2], 10);
    if (y != NaN && m != NaN && d != NaN) {
        return y
    }
    // return `${d}.${m}.${y}`

    // return new Date(y, m - 1, d);
}

// faqat lotin harflari raqamlar va belgilar

function LotinInputFilter(e) {

    var ew = e.which

    if (33 <= ew && ew <= 38) {
        e.preventDefault()
    } else if (91 <= ew && ew <= 96) {
        e.preventDefault()
    } else if (123 <= ew && ew <= 126) {
        e.preventDefault()
    } else if (186 <= ew && ew <= 222) {
        e.preventDefault()
    } else if (1040 <= ew && ew <= 1105) {
        $.notifyDefaults({
            type: 'danger',
            allow_dismiss: false,
            animate: {
                enter: 'animated fadeInRight',
                exit: 'animated fadeOutRight'
            },
            placement: {
                from: "top",
                align: "right"
            },
            z_index: 9999,
        })
        $.notify({
            icon: 'glyphicon glyphicon-star',
            message: '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-patch-exclamation" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\n' +
                '  <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>\n' +
                '  <path fill-rule="evenodd" d="M10.273 2.513l-.921-.944.715-.698.622.637.89-.011a2.89 2.89 0 0 1 2.924 2.924l-.01.89.636.622a2.89 2.89 0 0 1 0 4.134l-.637.622.011.89a2.89 2.89 0 0 1-2.924 2.924l-.89-.01-.622.636a2.89 2.89 0 0 1-4.134 0l-.622-.637-.89.011a2.89 2.89 0 0 1-2.924-2.924l.01-.89-.636-.622a2.89 2.89 0 0 1 0-4.134l.637-.622-.011-.89a2.89 2.89 0 0 1 2.924-2.924l.89.01.622-.636a2.89 2.89 0 0 1 4.134 0l-.715.698a1.89 1.89 0 0 0-2.704 0l-.92.944-1.32-.016a1.89 1.89 0 0 0-1.911 1.912l.016 1.318-.944.921a1.89 1.89 0 0 0 0 2.704l.944.92-.016 1.32a1.89 1.89 0 0 0 1.912 1.911l1.318-.016.921.944a1.89 1.89 0 0 0 2.704 0l.92-.944 1.32.016a1.89 1.89 0 0 0 1.911-1.912l-.016-1.318.944-.921a1.89 1.89 0 0 0 0-2.704l-.944-.92.016-1.32a1.89 1.89 0 0 0-1.912-1.911l-1.318.016z"/>\n' +
                '</svg> Faqat lotin harflar kiriting!'
        })
        e.preventDefault()
    }
}


// Ruxsat berilgan lotin bosh harflar, raqamlar
function PassportInputFilter(e) {
    var ew = e.which

    if (32 <= ew && ew <= 47) {
        e.preventDefault()
    } else if (58 <= ew && ew <= 64) {
        e.preventDefault()
    } else if (91 <= ew && ew <= 126) {
        $.notifyDefaults({
            type: 'danger',
            allow_dismiss: false,
            animate: {
                enter: 'animated fadeInRight',
                exit: 'animated fadeOutRight'
            },
            placement: {
                from: "top",
                align: "right"
            },
            z_index: 9999,
        })
        $.notify({
            icon: 'glyphicon glyphicon-star',
            message: '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-patch-exclamation" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\n' +
                '  <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>\n' +
                '  <path fill-rule="evenodd" d="M10.273 2.513l-.921-.944.715-.698.622.637.89-.011a2.89 2.89 0 0 1 2.924 2.924l-.01.89.636.622a2.89 2.89 0 0 1 0 4.134l-.637.622.011.89a2.89 2.89 0 0 1-2.924 2.924l-.89-.01-.622.636a2.89 2.89 0 0 1-4.134 0l-.622-.637-.89.011a2.89 2.89 0 0 1-2.924-2.924l.01-.89-.636-.622a2.89 2.89 0 0 1 0-4.134l.637-.622-.011-.89a2.89 2.89 0 0 1 2.924-2.924l.89.01.622-.636a2.89 2.89 0 0 1 4.134 0l-.715.698a1.89 1.89 0 0 0-2.704 0l-.92.944-1.32-.016a1.89 1.89 0 0 0-1.911 1.912l.016 1.318-.944.921a1.89 1.89 0 0 0 0 2.704l.944.92-.016 1.32a1.89 1.89 0 0 0 1.912 1.911l1.318-.016.921.944a1.89 1.89 0 0 0 2.704 0l.92-.944 1.32.016a1.89 1.89 0 0 0 1.911-1.912l-.016-1.318.944-.921a1.89 1.89 0 0 0 0-2.704l-.944-.92.016-1.32a1.89 1.89 0 0 0-1.912-1.911l-1.318.016z"/>\n' +
                '</svg> Faqat bosh harflar kiriting!'
        })
        e.preventDefault()
    } else if (1040 <= ew && ew <= 1105) {
        $.notifyDefaults({
            type: 'danger',
            allow_dismiss: false,
            animate: {
                enter: 'animated fadeInRight',
                exit: 'animated fadeOutRight'
            },
            placement: {
                from: "top",
                align: "right"
            },
            z_index: 9999,
        })
        $.notify({
            icon: 'glyphicon glyphicon-star',
            message: '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-patch-exclamation" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\n' +
                '  <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>\n' +
                '  <path fill-rule="evenodd" d="M10.273 2.513l-.921-.944.715-.698.622.637.89-.011a2.89 2.89 0 0 1 2.924 2.924l-.01.89.636.622a2.89 2.89 0 0 1 0 4.134l-.637.622.011.89a2.89 2.89 0 0 1-2.924 2.924l-.89-.01-.622.636a2.89 2.89 0 0 1-4.134 0l-.622-.637-.89.011a2.89 2.89 0 0 1-2.924-2.924l.01-.89-.636-.622a2.89 2.89 0 0 1 0-4.134l.637-.622-.011-.89a2.89 2.89 0 0 1 2.924-2.924l.89.01.622-.636a2.89 2.89 0 0 1 4.134 0l-.715.698a1.89 1.89 0 0 0-2.704 0l-.92.944-1.32-.016a1.89 1.89 0 0 0-1.911 1.912l.016 1.318-.944.921a1.89 1.89 0 0 0 0 2.704l.944.92-.016 1.32a1.89 1.89 0 0 0 1.912 1.911l1.318-.016.921.944a1.89 1.89 0 0 0 2.704 0l.92-.944 1.32.016a1.89 1.89 0 0 0 1.911-1.912l-.016-1.318.944-.921a1.89 1.89 0 0 0 0-2.704l-.944-.92.016-1.32a1.89 1.89 0 0 0-1.912-1.911l-1.318.016z"/>\n' +
                '</svg> Faqat lotin harflar kiriting!'
        })
        e.preventDefault()
    }
}


function InputMaxLength() {
    var $this = $(this);
    var maxlength = $this.attr('max').length;
    var value = $this.val();
    if (value && value.length >= maxlength) {
        $this.val(value.substr(0, maxlength));
    }
}


function instruction_sweet() {
    var html = `<p>Hurmatli foydalanuvchi ! <a href="/">Onless.uz</a> tizimidan foydalanish bo'yicha yo'riqnoma bilan tanishib chiqing!</p>
<p style="text-align:left">1.<a href="/video/categories/">Videodarslar</a> bo'limidagi barcha videolar to'liq oxirigacha ko'rilishi lozim.</p>
<p style="text-align:left">2.Videodars ostida mavzuga oid testlar bo'lsa shu testlarga javob berishingiz kerak. (Eslatma: Video oxirigacha ko'rilmasa test ochilmaydi)</p>
<p style="text-align:left">3.<a href="/quiz/select-lang/">Test savollari</a>  bo'limiga o'tib <a href="/quiz/select-type/?lang=uz&type=T">mashg'ulot rejimi</a>da har bir biletni yechib chiqish (Eslatma: Agar mavjud biletdagi 10 ta savolga 10 ta javob to'g'ri berilmasa keyingi bilet ochilmaydi)</p>
<p style="text-align:left">4.<a href="/quiz/select-type/?lang=uz&type=T">Mashg'ulot rejimi</a>da barcha biletlar ko'rib chiqilgandan so'ng <a href="/quiz/select-type/?lang=uz&type=I">imtihon rejimi</a>da o'zingizni sinovdan o'tkazing!</p>

<p style="text-align:left">Sizning video ostidagi testlarga bergan javoblaringiz avtomaktab nazoratida bo'ladi.</p>
<p style="text-align:left">Guruh rahbaringiz esa sizning o'zlashtirish darajangizga qarab sizning nazariy bilimlaringizni baholab boradi. Siz uchun tushunarsiz savol yoki mavzularga oid savollar yuzaga kelsa telegramdagi <a href="https://t.me/onless_support">yordam guruh</a>imizga yozib qoldiring.  Sizga mutahasislar yordam berishadi. Agarda tizim borasida savol va takliflaringiz bo'lsa <a href="https://t.me/Sirojiddin_Yakubov">Sirojiddin Yakubov</a>ga yozib qoldiring.</p>
<p style="text-align:left">Agar siz mobil telefon orqali bizning tizimizdan foydalanayotgan bo'lsangiz chap tomondagi menyu yopiq holatda turadi. Menyuni ochish uchun ekranning eng yuqori chap tomonida 3 ta chiziqcha qo'yilgan. Menyuni ochib menyudagi har bir bo'lim bilan tanishib chiqing!</p>
<p style="text-align:left">Bizning tizimdan foydalanish uchun sizga yuborilgan login va parolning logini sizning passport seriyangiz, parolni esa tizimning o'zi avtomatik holatda 7 xonali sondan iborat raqam generatsiya qilib qo'yadi. Agarda siz o'zingiz uchun esda qolarli parol yaratmoqchi bo'lsangiz. Menyuga kirib <a href="/user/settings/">tahrirlash</a> bo'limidan parolni o'zgartiring va saqlashga bosing.</p>`
    var swalButtonTitle = 'Tanishib chiqdim!'
    Swal.fire({
        title: 'Tizimdan foydalanish uchun qo\'llanma',
        text: '',
        width: 900,
        html: html,
        showClass: {
            popup: 'animate__animated animate__fadeInDown',

        },
        hideClass: {
            popup: 'animate__animated animate__fadeOutUp'
        },
        inputAttributes: {
            autocapitalize: 'off'
        },
        // {#customClass: 'swal-wide',#}
        showConfirmButton: true,
        focusConfirm: false,
        confirmButtonText: swalButtonTitle,
        confirmButtonColor: '#8b8989',
        allowOutsideClick: false,
        //  {#background: '#fff url(/images/trees.png)',#}
        //  {#backdrop: ``#}
        customClass: {
            backdrop: 'swal-wide',

        }

    })
}


// datepicker timepicker

function CreateNewDateExceptionSunday() {
    var get_date = new Date();
    if (get_date.getDay() === 0) {
        return new Date(new Date().setDate(new Date().getDate() + 1));
    } else {
        return get_date
    }
}

$(function () {

    $(".datepicker").datepicker({
        dateFormat: "dd.mm.yy",
        // minDate: '-90d',
        // maxDate: '+5M',
        // defaultDate: '01-01-1985',
        // value: "7/11/2011",
        showButtonPanel: true,
        numberOfMonths: 1,
        //startDate: "-30d",
        //endDate: "+30d",
        //currentText: 'Today',
        autoclose: true,
        changeMonth: false,
        changeYear: false,
        beforeShowDay: function (date) {
            var day = date.getDay();
            return [(day !== 0), ''];
        },
        onClose: function () {
            if ($(this).val().match(dateReg)) {
                $(this).css('border-color', 'green')
            } else {
                $(this).css('border-color', 'red')
            }
        }


        //gotoCurrent: true,
        //stepMonths: 0,
        //duration: 'fast',
        // yearRange: '1920:2030',

        // beforeShow: function () {
        //     alert('show');
        //    $("#ui-datepicker-div").addClass("DatePikerEN");
        //},


    })


    $(".datepicker").datepicker('setDate', CreateNewDateExceptionSunday());

    $(".starttimepicker").timepicker({
        timeFormat: 'H:mm',
        interval: 5,
        minTime: '08',
        maxTime: '22:00',
        defaultTime: '08',
        startTime: '08',
        dynamic: true,
        dropdown: true,
        scrollbar: true,
    });

    $(".stoptimepicker").timepicker({
        timeFormat: 'H:mm',
        interval: 5,
        minTime: '08',
        maxTime: '22:00',
        defaultTime: '10',
        startTime: '08',
        dynamic: true,
        dropdown: true,
        scrollbar: true,

    });
});

function parseDate(value) {
    var date = value.split("-");
    var y = parseInt(date[0], 10),
        m = parseInt(date[1], 10),
        d = parseInt(date[2], 10);
    if (y != NaN && m != NaN && d != NaN) {
        return y
    }
    // return `${d}.${m}.${y}`

    // return new Date(y, m - 1, d);
}

var dateReg = /^(0?[1-9]|[12][0-9]|3[01])[./-](0?[1-9]|1[012])[./-]\d{4}$/

// $('.datepicker_icon').on('click', function () {
//     $('.datepicker').datepicker('show')
// })

$('.datepicker').on('keypress', function (e) {
    return false
})

function errorFunction() {

    $.notifyDefaults({
        type: 'danger',
        allow_dismiss: false,
        z_index: '9999'
    })
    $.notify({
        icon: 'glyphicon glyphicon-star',
        message: '<svg width="1em" height="1em" viewBox="0 0 16 16" class="bi bi-patch-exclamation" fill="currentColor" xmlns="http://www.w3.org/2000/svg">\n' +
            '  <path d="M7.002 11a1 1 0 1 1 2 0 1 1 0 0 1-2 0zM7.1 4.995a.905.905 0 1 1 1.8 0l-.35 3.507a.552.552 0 0 1-1.1 0L7.1 4.995z"/>\n' +
            '  <path fill-rule="evenodd" d="M10.273 2.513l-.921-.944.715-.698.622.637.89-.011a2.89 2.89 0 0 1 2.924 2.924l-.01.89.636.622a2.89 2.89 0 0 1 0 4.134l-.637.622.011.89a2.89 2.89 0 0 1-2.924 2.924l-.89-.01-.622.636a2.89 2.89 0 0 1-4.134 0l-.622-.637-.89.011a2.89 2.89 0 0 1-2.924-2.924l.01-.89-.636-.622a2.89 2.89 0 0 1 0-4.134l.637-.622-.011-.89a2.89 2.89 0 0 1 2.924-2.924l.89.01.622-.636a2.89 2.89 0 0 1 4.134 0l-.715.698a1.89 1.89 0 0 0-2.704 0l-.92.944-1.32-.016a1.89 1.89 0 0 0-1.911 1.912l.016 1.318-.944.921a1.89 1.89 0 0 0 0 2.704l.944.92-.016 1.32a1.89 1.89 0 0 0 1.912 1.911l1.318-.016.921.944a1.89 1.89 0 0 0 2.704 0l.92-.944 1.32.016a1.89 1.89 0 0 0 1.911-1.912l-.016-1.318.944-.921a1.89 1.89 0 0 0 0-2.704l-.944-.92.016-1.32a1.89 1.89 0 0 0-1.912-1.911l-1.318.016z"/>\n' +
            '</svg> Xatolik yuz berdi! Sahifani yangilab qayta urinib ko\'ring'
    })
}


function success_toast(success_url) {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        background: '#8ff8ac',
        timer: 5000,
        timerProgressBar: false,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        },
        // willClose: (close) => {
        //    window.location.href = success_url
        // }
    })
    Toast.fire({
        icon: 'success',
        title: 'Muvaffaqiyatli saqlandi!'
    })
}

function edit_toast() {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        showConfirmButton: false,
        background: '#8ff8ac',
        timer: 5000,
        timerProgressBar: false,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        },
        // willClose: (close) => {
        //    window.location.href = success_url
        // }
    })
    Toast.fire({
        icon: 'success',
        title: 'Muvaffaqiyatli tahrirlandi!'
    })
}

function error_toast() {
    const Toast = Swal.mixin({
        toast: true,
        position: 'top-end',
        background: '#ffa2a2',
        showConfirmButton: false,
        timer: 5000,
        timerProgressBar: false,
        didOpen: (toast) => {
            toast.addEventListener('mouseenter', Swal.stopTimer)
            toast.addEventListener('mouseleave', Swal.resumeTimer)
        }
    })
    Toast.fire({
        icon: 'error',
        title: 'Bekor qilindi!'
    })
}


function add_payment(create_url, success_url, e) {

    e.preventDefault()
    const {value: formValues} = Swal.fire({
        allowOutsideClick: false,
        showCancelButton: true,
        showLoaderOnConfirm: true,
        showClass: {
            popup: 'animate__animated animate__fadeInDown'
        },
        hideClass: {
            popup: 'animate__animated animate__fadeOutUp'
        },
        confirmButtonText: 'Keyingi',
        cancelButtonText: 'Bekor qilish',
        reverseButtons: true,
        title: 'To\'lov summasini kiriting!',
        html:
            '<label style="float: left; margin-bottom: 0" class="label_required" for="amount">Summa</label>' +
            '<input style="margin-top: 4px" id="amount" class="form-control" type="number" placeholder="Masalan: 100000">',

        focusConfirm: false,
        preConfirm: (value) => {
            if (value) {
                if ($('#amount').val() == '') {
                    Swal.showValidationMessage(
                        'Summa kiritilmagan!'
                    )
                } else if ($('#amount').val() < 5000) {
                    Swal.showValidationMessage(
                        'Summa kamida 5000 so\'m bo\'lishi kerak!'
                    )
                } else {
                    swal.resetValidationMessage();
                    return [
                        $('#amount').val()
                    ]
                }
            }

            $('#amount').on('keyup', function () {
                if ($('#amount').val() == '') {
                    Swal.showValidationMessage(
                        'Summa kiritilmagan!'
                    )
                } else if ($('#amount').val() < 5000) {
                    Swal.showValidationMessage(
                        'Summa kamida 5000 so\'m bo\'lishi kerak!'
                    )
                } else {
                    swal.resetValidationMessage();

                }
            })
        },

    }).then(function (confirm) {

        if (confirm.isConfirmed) {
            var amount = confirm.value[0]

            window.location.href = create_url + "?amount=12345".replace(/12345/, amount.toString());

        } else {
            window.location.href = success_url
        }

    })
}