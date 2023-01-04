import Vue from 'vue';
class WeblogMessageService {
    constructor() {
      this.messages = Vue.observable({
        items : ["testmessage"]
      })
    }
  
    addMessage(message) {
      this.messages.items.push(message);
      // set(this.messages, this.messages.length, message);
    }

    receiveMessage(message) {
        console.log("Received message.", message)
        this.addMessage(message)
    }
  }
  
  export default new WeblogMessageService();
