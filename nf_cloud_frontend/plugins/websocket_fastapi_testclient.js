import weblogMessageService from '@/service/weblog-message-service';


export default ({ app }, inject) => {
    var client_id = Date.now()
    const fastapi_socket = new WebSocket(`ws://localhost:8765/ws/${client_id}`);

      fastapi_socket.onmessage = function(event) {
        console.log(weblogMessageService);
        weblogMessageService.receiveMessage(event.data);
        console.log(event.data);
      };
    
      inject('fastapi_socket', fastapi_socket)
}
