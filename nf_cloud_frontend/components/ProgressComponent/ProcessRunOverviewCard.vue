<template>
  <div>
    <div class="card-container">
      <div class="card">
        <div class="card-header">Run {{ runname }}</div>
        <div class="card-body">{{ messagesOfRun }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import weblogMessageService from "@/service/weblog-message-service";

export default {
  name: "ProcessRunOverviewCard",
  props: {
    runname: {
      type: String,
      required: true,
    },
  },

  computed: {
    messages() {
      return weblogMessageService.messages.items;
    },
    messagesOfRun() {
      return weblogMessageService.filterMessagesByRunName(this.messages, this.runname);
    },
  },
  data() {
    return {};
  },
  methods: {},
};
</script>

<style lang="scss" scoped></style>
