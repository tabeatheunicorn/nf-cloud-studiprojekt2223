<template>
  <ul>
    <li v-for="(message, index) in messages" :key="index">{{ message }}</li>
  </ul>
</template>

<script>
import weblogMessageService from "@/service/weblog-message-service";

export default {
  name: "WeblogMessageList",
  computed: {
    messages() {
      return weblogMessageService.messages.items;
    },
  },
};
</script>
