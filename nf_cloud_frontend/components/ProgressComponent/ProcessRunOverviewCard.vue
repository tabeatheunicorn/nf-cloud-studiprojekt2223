<template>
  <div>
    <div class="card-container">
      <div class="card">
        <div class="card-header">Run {{ runname }}</div>
        <div class="card-body">
          <p>Running since {{ firstMessageTimestamp }}</p>
          <p>
            <template v-if="lastMessageTimestamp">
              Run until {{ lastMessageTimestamp }}
            </template>
            <template v-else>
              <timer-component :start-time="firstMessageTimestamp" />
            </template>
          </p>
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
import TimerComponent from "@/components/ProgressComponent/TimerComponent.vue";

export default {
  name: "ProcessRunOverviewCard",
  components: { WeblogMessageList, TimerComponent },
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
