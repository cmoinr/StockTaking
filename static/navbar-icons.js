document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.icon-btn').forEach(function(btn) {
        btn.addEventListener('mouseenter', function() {
            btn.classList.add('icon-btn-extended');
        });
        btn.addEventListener('mouseleave', function() {
            btn.classList.remove('icon-btn-extended');
        });
        btn.addEventListener('focus', function() {
            btn.classList.add('icon-btn-extended');
        });
        btn.addEventListener('blur', function() {
            btn.classList.remove('icon-btn-extended');
        });
    });
});
