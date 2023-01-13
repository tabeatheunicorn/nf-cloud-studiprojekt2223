<template>
  <div>
    <div class="card-container">
      <div class="card">
        <div class="card-header">Run {{ runname }}</div>
        <div class="card-body">
          <p>Running since {{ firstMessageTimestamp }}</p>
          <p>Run until {{ lastMessageTimestamp }}</p>
          <button @click="showMessages = !showMessages">
            {{ showMessages ? "Hide" : "Show" }} messages
          </button>
          <weblog-message-list v-if="showMessages" :runName="runname" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import weblogMessageService from "@/service/weblog-message-service";
import WeblogMessageList from "@/components/ProgressComponent/WeblogMessageList";

export default {
  name: "ProcessRunOverviewCard",
  components: { WeblogMessageList },
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
    firstMessageTimestamp() {
      return weblogMessageService.getFirstSubmittedMessage(this.messages, this.runname);
    },
    lastMessageTimestamp() {
      return weblogMessageService.getFirstCompletedMessage(this.messages, this.runname);
    },
  },
  data() {
    return {
      showMessages: false,
    };
  },
  methods: {},
};
</script>

<style lang="scss" scoped></style>
