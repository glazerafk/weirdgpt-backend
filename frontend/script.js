const input = document.getElementById('user-input');
const chat = document.getElementById('chat');

input.addEventListener('keydown', async (e) => {
    if(e.key === 'Enter'){
        const msg = input.value.trim();
        if(!msg) return;
        chat.innerHTML += '<div><b>You:</b> ' + msg + '</div>';
        input.value = '';

        const res = await fetch('/api/chat', {
            method:'POST',
            headers:{'Content-Type':'application/json'},
            body: JSON.stringify({message: msg})
        });
        const data = await res.json();
        chat.innerHTML += '<div><b>WeirdGPT:</b> ' + data.reply + '</div>';
        chat.scrollTop = chat.scrollHeight;
    }
});
