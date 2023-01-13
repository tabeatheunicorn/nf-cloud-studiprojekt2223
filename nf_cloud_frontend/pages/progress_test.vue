<template>
  <div>
    <h1>Test Overview for Weblog Messages</h1>
    <websocket-connection-info-modal />
    <div id="progresgraph"></div>
    <status-overview-weblog-messages />
    <process-run-overview-card :runname="'grave_visvesvaraya'" />
    <weblog-message-list />
  </div>
</template>

<script>
import WebsocketConnectionInfoModal from "@/components/ProgressComponent/WebsocketConnectionInfoModal.vue";
import WeblogMessageList from "@/components/ProgressComponent/WeblogMessageList.vue";
import StatusOverviewWeblogMessages from "@/components/ProgressComponent/StatusOverviewWeblogMessages";
import ProcessRunOverviewCard from "@/components/ProgressComponent/ProcessRunOverviewCard";

export default {
  components: {
    WebsocketConnectionInfoModal,
    WeblogMessageList,
    StatusOverviewWeblogMessages,
    ProcessRunOverviewCard,
  },
  mounted() {
    var plot_data = [
      {
        type: "treemap",
        labels: ["Eve", "Cain", "Seth", "Enos", "Noam", "Abel", "Awan", "Enoch", "Azura"],
        parents: ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"],
      },
    ];
    var plot_layout = { title: "My graph" };
    var plot_config = {
      responsive: true,
    };
    this.$plotly.newPlot("progresgraph", plot_data, plot_layout, plot_config);
  },
};
</script>
