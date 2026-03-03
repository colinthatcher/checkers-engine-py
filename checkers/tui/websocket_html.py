html = """
<!DOCTYPE html>
<html>
<head>
    <title>Chat</title>
</head>
<body>
    <h1>WebSocket with FastAPI</h1>
    <form action="" onsubmit="sendMessage(event)">
        <input type="text" id="messageText" autocomplete="off" />
        <button>Send</button>
    </form>
    <ul id='messages'>
    </ul>
    <script>
        console.log("Init socket...");

        var ws = new WebSocket(`ws://localhost:8000/communicate/1234`);
        ws.onopen = () => {
            console.log("Connected to socket!");
        };

        ws.onerror = (err) => {
            console.log("Error using socket!");
            console.error(err);
        };
        
        ws.onmessage = function (event) {
            var messages = document.getElementById('messages');
            var message = document.createElement('li');
            var content = document.createTextNode(event.data);
            message.appendChild(content);
            messages.appendChild(message);
        };

        function sendMessage(event) {
            console.log("Send Message trigger");
            var input = document.getElementById("messageText");
            ws.send(input.value);
            input.value = '';
            event.preventDefault();
        }
    </script>
</body>
</html>
"""
