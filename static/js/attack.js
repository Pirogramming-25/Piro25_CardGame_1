let selectedCard = null;

fetch("/games/cards/")
.then(response => response.json())
.then(data => {

    const cardList = document.getElementById("card-list");

    data.cards.forEach(card => {

        const div = document.createElement("div");

        div.className = "card";
        div.innerText = card;

        div.onclick = function(){

            document.querySelectorAll(".card").forEach(c=>{
                c.classList.remove("selected");
            });

            div.classList.add("selected");

            selectedCard = card;
        };

        cardList.appendChild(div);

    });

});


document.getElementById("attack-btn").onclick = function(){

    const target = document.getElementById("target-user").value;

    fetch("/games/attack/",{

        method:"POST",

        headers:{
            "Content-Type":"application/json"
        },

        body:JSON.stringify({

            target_user:target,
            attacker_card:selectedCard

        })

    })
    .then(response=>response.json())
    .then(data=>{

        alert(data.message);

    });

};