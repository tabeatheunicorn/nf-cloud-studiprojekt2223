<template>
  <ul>
    <li v-for="message in messages" :key="message">{{ message }}</li>
  </ul>
</template>

<script>
import weblogMessageService from "@/service/weblog-message-service";

export default {
  name: "WeblogMessageList",
  computed: {
    messages() {
      return weblogMessageService.messages;
    },
  },
};
</script>
