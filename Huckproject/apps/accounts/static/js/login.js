document.addEventListener('DOMContentLoaded', function() {
    // グローバル変数として定義されたmessagesArrayを使用
    if (typeof messagesArray !== 'undefined' && messagesArray.length > 0) {
        messagesArray.forEach(function(message) {
            alert(message);
        });
    }
}); 