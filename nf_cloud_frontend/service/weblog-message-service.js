import Vue from 'vue';
class WeblogMessageService {
  constructor() {
    this.messages = Vue.observable({
      items: []
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

  /*
  Multiple helper functions that can probably be moved to the service because these are needed by more
  components ultimately.
  */
  filterMessagesByTraceStatus(messages, status) {
    const filtered = messages.filter(
      (message) => message.trace && message.trace.status === status
    );
    return filtered;
  }

  filterMessagesByRunName(messages, runName) {
    const filtered = messages.filter(
      (message) => message.runName && message.runName === runName
    );
    return filtered;
  }

  filterMessagesByProcessTaskID(messages, process, taskID = undefinded) {
    let filtered = messages.filter(
      (message) => message.trace && message.trace.process === process
    );
    if (taskID !== undefined) {
      filtered = filtered.filter((message) => message.trace.taskID === taskID);
    }
    return filtered;
  }

  getUniqueNames(messages){
    return [...new Set(messages.map((message) => message.runName))];
  }
}

export default new WeblogMessageService();
