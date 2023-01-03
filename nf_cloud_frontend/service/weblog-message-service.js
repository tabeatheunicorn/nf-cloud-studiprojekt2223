class WeblogMessageService {
    constructor() {
      this.messages = ["testmessage"]
    }
  
    addMessage(message) {
      this.messages.push(message)
    }

    receiveMessage(message) {
        console.log("Received message.", message)
        this.addMessage(message)
    }
  }
  
  export default new WeblogMessageService()