<template>
  <div>Number of messages: {{ messages.length }}</div>
</template>

<script>
import weblogMessageService from "@/service/weblog-message-service";

export default {
  name: "StatusOverviewWeblogMessages",
  computed: {
    messages() {
      return weblogMessageService.messages.items;
    },
  },
};
</script>
