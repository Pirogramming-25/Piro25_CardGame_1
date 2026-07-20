// ===============================
// CSRF TOKEN
// ===============================

const csrftoken = document.querySelector(
    '[name=csrfmiddlewaretoken]'
).value;


// ===============================
// 반격 모달 요소
// ===============================

const modalOverlay = document.getElementById("counter-modal-overlay");
const cardListEl = document.getElementById("counter-card-list");
const submitBtn = document.getElementById("counter-attack-submit-btn");
const currentUsername = modalOverlay.dataset.currentUser;

let currentAttackId = null;


function openCounterModal(attackId) {
    currentAttackId = attackId;
    cardListEl.innerHTML = "";

    fetch("/games/cards/")
        .then(response => response.json())
        .then(data => {

            data.cards.forEach(card => {

                const label = document.createElement("label");
                label.className = "counter-card-option";

                const input = document.createElement("input");
                input.type = "radio";
                input.name = "counter-card";
                input.value = card;

                label.appendChild(input);
                label.appendChild(document.createTextNode(card));

                cardListEl.appendChild(label);
            });

        })
        .catch(error => {
            console.log(error);
            alert("카드를 불러오는데 실패했습니다.");
        });

    modalOverlay.classList.remove("hidden");
}


function closeCounterModal() {
    modalOverlay.classList.add("hidden");
    currentAttackId = null;
}


// ===============================
// CounterAttack 버튼 클릭 -> 모달 오픈
// ===============================

document.querySelectorAll(".counter-attack-btn").forEach(btn => {
    btn.onclick = function () {
        openCounterModal(btn.dataset.attackId);
    };
});


// ===============================
// 취소 버튼 클릭 -> 보낸 공격 취소
// ===============================

document.querySelectorAll(".cancel-attack-btn").forEach(btn => {
    btn.onclick = function () {

        if (!confirm("공격 신청을 취소하시겠습니까?")) {
            return;
        }

        fetch(`/games/cancel/${btn.dataset.attackId}/`, {

            method: "POST",

            headers: {
                "X-CSRFToken": csrftoken
            }

        })

        .then(response => response.json())

        .then(data => {

            if (data.error) {
                alert(data.error);
                return;
            }

            alert(data.message);
            window.location.href = "/games/game_list/";

        })

        .catch(error => {
            console.log(error);
            alert("취소 실패");
        });

    };
});


// ===============================
// 대결 상세 모달
// ===============================

const finishedMatches = JSON.parse(
    document.getElementById("finished-matches-data").textContent
);

const matchDetailOverlay = document.getElementById("match-detail-overlay");


function formatChange(value) {
    if (value > 0) return `+${value}`;
    if (value < 0) return `${value}`;
    return "±0";
}


function changeClass(value) {
    if (value > 0) return "positive";
    if (value < 0) return "negative";
    return "neutral";
}


function openMatchDetail(match) {
    document.getElementById("detail-attacker").textContent = match.attacker;
    document.getElementById("detail-defender").textContent = match.defender;

    document.getElementById("detail-attacker-card").textContent = match.attacker_card;
    document.getElementById("detail-defender-card").textContent = match.defender_card;

    const attackerChangeEl = document.getElementById("detail-attacker-change");
    attackerChangeEl.textContent = formatChange(match.attacker_change);
    attackerChangeEl.className = "match-card-change " + changeClass(match.attacker_change);

    const defenderChangeEl = document.getElementById("detail-defender-change");
    defenderChangeEl.textContent = formatChange(match.defender_change);
    defenderChangeEl.className = "match-card-change " + changeClass(match.defender_change);

    document.getElementById("detail-criteria").textContent = match.criteria_text;

    document.getElementById("detail-winner").textContent = match.is_draw
        ? "승자 없음"
        : `${match.winner} 승리`;

    matchDetailOverlay.classList.remove("hidden");
}


document.querySelectorAll(".match-detail-btn").forEach(btn => {
    btn.onclick = function () {
        openMatchDetail(finishedMatches[Number(btn.dataset.index)]);
    };
});


document.getElementById("match-detail-close-btn").onclick = function () {
    matchDetailOverlay.classList.add("hidden");
};


matchDetailOverlay.onclick = function (event) {
    if (event.target === matchDetailOverlay) {
        matchDetailOverlay.classList.add("hidden");
    }
};


// ===============================
// 오버레이 바깥 클릭 -> 모달 닫기
// ===============================

modalOverlay.onclick = function (event) {
    if (event.target === modalOverlay) {
        closeCounterModal();
    }
};


// ===============================
// 반격 제출
// ===============================

submitBtn.onclick = function () {

    const selected = cardListEl.querySelector('input[name="counter-card"]:checked');

    if (!selected) {
        alert("카드를 선택하세요!");
        return;
    }

    fetch(`/games/counter/${currentAttackId}/`, {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken
        },

        body: JSON.stringify({
            defender_card: Number(selected.value)
        })

    })

    .then(response => response.json())

    .then(data => {

        if (data.error) {
            alert(data.error);
            return;
        }

        const winner = data.winner;

        if (winner === null) {
            alert("무승부입니다!");
        } else if (winner === currentUsername) {
            alert("승리했습니다!");
        } else {
            alert(`${winner}님이 승리했습니다.`);
        }

        window.location.href = "/games/game_list/";

    })

    .catch(error => {
        console.log(error);
        alert("반격 실패");
    });

};
