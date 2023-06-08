$(document).ready(function () {
    listing();
});

function listing() {
    fetch("/room/list").then((res) => res.json()).then((data) => {
        let rooms = JSON.parse(data['result'])
        console.log(rooms)
        rooms.forEach((a) => {
            let room_id = a['_id']['$oid']
            let max_people = a['max_people']
            let prt = a['prt']
            let room_info = a['room_info']
            let room_name = a['room_name']
            let prt_users = a['prt_users']

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
                                    <button onclick="location.href='/board/${room_id}'" class="btn btn-outline-dark" type="button" style="float : right">
                                        입장
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
                                    <button onclick="join('${room_id}')" class="btn btn-outline-dark" type="button" style="float : right">
                                        참가
                                    </button>
                                </td>
                            </tr>`
            }
            $('#order-box').append(temp_html)
        })

    });
}
function join(room_id) {
    // let user_id = "nobi1" //임시
    let formData = new FormData();
    // formData.append("user_id", user_id); //임시
    formData.append("room_id", room_id);

    fetch('/room/join', { method: "UPDATE", body: formData }).then((res) => res.json()).then((data) => {
        alert(data['msg'])
        window.location.reload()
    })
}