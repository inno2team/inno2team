$(document).ready(function () {
    listing();
});

function listing() {
    fetch("/mypage/room/list").then((res) => res.json()).then((data) => {
        let rooms = JSON.parse(data['result'])
        console.log(rooms)
        rooms.forEach((a) => {
            let room_id = a['_id']['$oid']
            let max_people = a['max_people']
            let prt = a['prt']
            let room_info = a['room_info']
            let room_name = a['room_name']

            let temp_html = ``

            if (prt == max_people) {
                // 정원이 가득일때
                temp_html = `<tr>
                                <td>${room_name}</td>
                                <td>
                                    ${room_info}
                                </td>
                                <td>
                                    <img class="full"
                            src="https://spconsulting.ca/wp-content/uploads/2022/08/end.png">
                                    <button onclick="delete_room('${room_id}')" class="btn btn-outline-danger" type="button" style="float : right">
                                        삭제
                                    </button>
                                </td>
                            </tr>`
            } else {
                temp_html = `<tr>
                                <td>${room_name}</td>
                                <td>
                                    ${room_info}
                                </td>
                                <td>
                                    ${prt} / ${max_people}
                                    <button onclick="delete_room('${room_id}')" class="btn btn-outline-danger" type="button" style="float : right">
                                        삭제
                                    </button>
                                </td>
                            </tr>`
            }
            $('#order-box').append(temp_html)
        })

    });
}

function delete_room(room_id) {
    let formData = new FormData();
    formData.append('room_id', room_id)
    fetch('/delete', { method: "POST", body: formData })
        .then(response => response.json())
        .then(data => {
            alert(data["msg"]);
            window.location.reload();
        })
}

function change_info() {
    let password = $('#password').val();
    let new_password = $('#new_password').val();
    let nickname = $('#nickname').val();
    let phone = $('#phone').val();

    let formData = new FormData();
    formData.append("password_give", password);
    formData.append("new_password_give", new_password);
    formData.append("nickname_give", nickname);
    formData.append("phone_give", phone);

    fetch('/mypage/update', { method: "UPDATE", body: formData })
        .then((response) => response.json())
        .then((data) => {
            let msg = data['msg']
            if (msg === '수정 완료') {
                window.location.href = "/"
            }
            else {
                window.location.reload();
            }
            alert(data["msg"])
        })
}

