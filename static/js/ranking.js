/* ranking 페이지 js */
/* 전체 틀 만든 뒤에 작성할 예정 */

(function () {
    const listEl = document.getElementById('ranking-list');
    const noDataEl = document.getElementById('no-data-msg');
    const dataUrl = listEl ? listEl.dataset.rankingUrl : null;
    const POLL_INTERVAL_MS = 5000; // 5초마다 갱신. 필요에 맞게 조절.

    function render(users) {
        if (!users || users.length === 0) {
            listEl.innerHTML = '';
            noDataEl.style.display = 'block';
            return;
        }

        noDataEl.style.display = 'none';
        listEl.innerHTML = users.map(function (u) {
            return (
                '<li class="ranking-item">' +
                    '<span class="rank-info">' +
                        '<span class="rank-num">' + u.rank + '.</span>' +
                        '<span class="rank-name">' + u.username + '</span>' +
                    '</span>' +
                    '<span class="rank-score">score: ' + u.score + '</span>' +
                '</li>'
            );
        }).join('');

        // 새로 그린 유저 이름에도 한글 wrap 다시 적용
        if (window.wrapKoreanText) {
            listEl.querySelectorAll('.rank-name').forEach(window.wrapKoreanText);
        }
    }

    function fetchRanking() {
        if (!dataUrl) return;

        fetch(dataUrl)
            .then(function (res) { return res.json(); })
            .then(function (data) { render(data.users); })
            .catch(function (err) { console.error('랭킹 갱신 실패:', err); });
    }

    if (listEl) {
        setInterval(fetchRanking, POLL_INTERVAL_MS);
    }
})();