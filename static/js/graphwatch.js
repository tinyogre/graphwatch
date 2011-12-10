var render;

function start_graph() {
    render = new graphrender();
    var sock = new io.Socket(window.location.hostname, {port: 11001, rememberTransport: false});
    sock.connect();
    sock.addEvent('connect', function() {
            sock.send({notice: 'I connected!'});
        });
    sock.addEvent('message', function(data) {
            if(data.newNode) {
                render.addNode(data.newNode);
            }
        });
}
    