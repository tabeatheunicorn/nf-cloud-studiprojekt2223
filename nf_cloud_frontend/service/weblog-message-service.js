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

  getUniqueNames(messages) {
    return [...new Set(messages.map((message) => message.runName))];
  }

  /**
   * getFirstSubmittedMessage - returns the utcTime property of the first message
   * that matches the specified conditions.
   *
   * @param  {Array} messages  an array of messages
   * @param  {String} runName  the runName to be matched
   * @return {String | null}  returns utcTime property of the first matched message or null if not found
   */
  getFirstSubmittedMessage(messages, runName) {
    const message = messages.find(message => 
      message.runName && message.runName === runName && 
      message.event && message.event === "started"
    )
    return message ? message.utcTime : null
  }

  getFirstCompletedMessage(messages, runName){
    const message = messages.find(message => 
      message.runName && message.runName === runName && 
      message.event && message.event === "completed"
    )
    return message ? message.utcTime : null
  }
}

export default new WeblogMessageService();
