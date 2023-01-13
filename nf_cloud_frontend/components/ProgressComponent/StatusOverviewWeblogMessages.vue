<template>
  <div>
    <h2>Message Info</h2>
    Number of messages: {{ messages.length }}

    <h2>Runs detected:</h2>
    <div v-for="runName in uniqueRunNames" :key="runName">
      {{ runName }}
    </div>

    <div>
      <label for="run-name-selector">Select run name:</label>
      <select id="run-name-selector" v-model="selectedRunName">
        <option v-for="runName in uniqueRunNames" :key="runName">{{ runName }}</option>
      </select>
    </div>

    <h2>Execution Status</h2>
    <div class="card-container">
      <div class="card">
        <div class="card-header">Scheduled</div>
        <div class="card-body">{{ scheduledMessages.length }}</div>
      </div>
      <div
        class="card"
        :class="{
          yellow: runningMessages.length < scheduledMessages.length,
          green: runningMessages.length >= scheduledMessages.length,
        }"
      >
        <div class="card-header">Running</div>
        <div class="card-body">
          {{ runningMessages.length }} / {{ scheduledMessages.length }}
        </div>
      </div>
      <div
        class="card"
        :class="{
          yellow: completedMessages.length < scheduledMessages.length,
          green: completedMessages.length >= scheduledMessages.length,
        }"
      >
        <div class="card-header">Completed</div>
        <div class="card-body">
          {{ completedMessages.length }} / {{ scheduledMessages.length }}
        </div>
      </div>
    </div>
  </div>
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
  data() {
    return {
      selectedRunName: "",
    };
  },
  computed: {
    messages() {
      return weblogMessageService.messages.items;
    },
    scheduledMessages() {
      return weblogMessageService.filterMessagesByTraceStatus(this.messages, "SUBMITTED");
    },
    runningMessages() {
      return weblogMessageService.filterMessagesByTraceStatus(this.messages, "RUNNING");
    },
    completedMessages() {
      return weblogMessageService.filterMessagesByTraceStatus(this.messages, "COMPLETED");
    },
    uniqueRunNames() {
      return weblogMessageService.getUniqueNames(this.messages);
    },
  },
};
</script>
