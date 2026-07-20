// Django CSRF Token 가져오기
const csrftoken = document.querySelector(
    '[name=csrfmiddlewaretoken]'
).value;


let selectedCard = null;




// 카드 가져오기
fetch("/games/cards/")
.then(response => response.json())
.then(data => {


    const cardList = document.getElementById("card-list");


    data.cards.forEach(card => {


        const div = document.createElement("div");


        div.className = "card";


        div.innerText = card;



        div.onclick = function(){


            // 기존 카드 선택 제거
            document.querySelectorAll(".card").forEach(c => {

                c.classList.remove("selected");

            });



            // 현재 카드 선택
            div.classList.add("selected");



            selectedCard = card;


        };



        cardList.appendChild(div);


    });


})


.catch(error => {


    console.log(error);


    alert("카드를 불러오는데 실패했습니다.");


});







// 공격 버튼 클릭
document.getElementById("attack-btn").onclick = function(){


    const target =
        document.getElementById("target-user").value;



    // 카드 선택 확인
    if (!selectedCard) {


        alert("카드를 선택하세요!");


        return;

    }




    // 유저 선택 확인
    if (!target) {


        alert("공격할 유저를 선택하세요!");


        return;

    }






    fetch("/games/attack/", {


        method: "POST",



        headers: {


            "Content-Type": "application/json",


            "X-CSRFToken": csrftoken


        },



        body: JSON.stringify({


            target_user: target,


            attacker_card: selectedCard


        })


    })



    .then(response => {


        if (!response.ok) {


            return response.text().then(text => {

                throw new Error(text);

            });


        }



        return response.json();


    })



    .then(data => {


        alert(data.message);


    })



    .catch(error => {


        console.log(error);


        alert("공격 실패");


    });


};