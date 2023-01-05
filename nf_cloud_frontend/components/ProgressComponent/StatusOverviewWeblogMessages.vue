<template>
  <div>
  Number of messages: {{ messages.length }}  
  <div class="card-container">
    <div class="card">
      <div class="card-header">Scheduled</div>
      <div class="card-body">{{ scheduledMessages.length }}</div>
    </div>
    <div class="card" :class="{ 'yellow': runningMessages.length < scheduledMessages.length, 'green': runningMessages.length >= scheduledMessages.length }">
      <div class="card-header">Running</div>
      <div class="card-body">{{ runningMessages.length }} / {{ scheduledMessages.length }}</div>
    </div>
    <div class="card" :class="{ 'yellow': completedMessages.length < scheduledMessages.length, 'green': completedMessages.length >= scheduledMessages.length }">
      <div class="card-header">Completed</div>
      <div class="card-body">{{ completedMessages.length }} / {{ scheduledMessages.length }}</div>
    </div>
  </div></div>

</template>

<style>
.card-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-evenly;
}

  .card {
  margin: 1em;
  /* Other styles for the card */
}
.yellow {
  background-color: yellow;
}

.green {
  background-color: rgb(141, 174, 16); /* Rub green */
}
</style>

<script>
import weblogMessageService from "@/service/weblog-message-service";

export default {
  name: "StatusOverviewWeblogMessages",
  computed: {
    messages() {
      return weblogMessageService.messages.items;
    },
    scheduledMessages() {
      const filtered = this.messages.filter((message) => message.trace  && message.trace.status === "SUBMITTED");
      return filtered;
    },
    runningMessages() {
      return this.messages.filter((message) => message.trace && message.trace.status === "RUNNING");
    },
    completedMessages() {
      return this.messages.filter((message) => message.trace && message.trace.status === "COMPLETED");
    },
  },
};
</script>
