
window.wrapKoreanText = function (el) {
    if (!el) return;
    el.innerHTML = el.textContent.replace(
        /([가-힣]+)/g,
        '<span class="ko-text">$1</span>'
    );
};
 
window.wrapKoreanTextAll = function (selector) {
    document.querySelectorAll(selector).forEach(window.wrapKoreanText);
};
 
document.addEventListener('DOMContentLoaded', function () {
    window.wrapKoreanTextAll('.main-user-info');
    window.wrapKoreanTextAll('.rank-name');
});
 