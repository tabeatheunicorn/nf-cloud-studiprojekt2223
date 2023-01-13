<template>
  <ul>
    <li v-for="(message, index) in filteredMessages" :key="index">{{ message }}</li>
  </ul>
</template>

<script>
import weblogMessageService from "@/service/weblog-message-service";

export default {
  name: "WeblogMessageList",
  props: {
    runName: {
      type: String,
      default: null,
    },
  },
  computed: {
    messages() {
      return weblogMessageService.messages.items;
    },
    filteredMessages() {
      return this.runName
        ? this.messages.filter((message) => message.runName === this.runName)
        : this.messages;
    },
  },
};
</script>
