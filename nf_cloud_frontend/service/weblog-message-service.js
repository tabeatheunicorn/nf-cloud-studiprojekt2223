import Vue from 'vue';
class WeblogMessageService {
    constructor() {
      this.messages = Vue.observable({
        items : []
      })
    }
  
    addMessage(message) {
      this.messages.items.push(message);
      // set(this.messages, this.messages.length, message);
    }

    receiveMessage(message) {
      const new_element = JSON.parse(message);
      this.addMessage(new_element);
    }
  }
  
  export default new WeblogMessageService();
