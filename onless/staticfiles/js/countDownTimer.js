let countdowntime = 900;
let Time = 0
let p = document.getElementById('countDown')
let p2 = document.getElementById('countdown')

let interval = setInterval(updateCountDown, 1000)

function updateCountDown() {
    let minutes = Math.floor(countdowntime / 60)
    let seconds = countdowntime % 60

    let finishMinutes = Math.floor(Time / 60)
    let finishSeconds = Time % 60

    seconds = seconds < 10 ? '0' + seconds : seconds
    minutes = minutes < 10 ? '0' + minutes : minutes

    finishSeconds = finishSeconds < 10 ? '0' + finishSeconds : finishSeconds
    finishMinutes = finishMinutes < 10 ? '0' + finishMinutes : finishMinutes
    p.innerHTML = `${minutes}:${seconds}`
    p2.innerHTML = `${finishMinutes}:${finishSeconds}`


    countdowntime--;
    Time++;

    if (countdowntime < 0) {
        clearInterval(interval)

        Swal.fire({
            // {#icon: 'error',#}
            title: FalseTitle,
            // {#background: '#ffecec',#}
            text: swalText,
            html: html,
            // {#timer: 2000,#}
            showConfirmButton: true,
            confirmButtonText: swalButtonTitle,
            // {#confirmButtonColor: '#a5c7f6',#}
            // {#footer: footerMsg,#}
        }).then(function (isConfirm) {
            if (isConfirm) {
                window.location.href = window.location.href;
            }
        })


    }

}