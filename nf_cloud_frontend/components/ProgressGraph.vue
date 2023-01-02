<template>
  <div id="progresgraph"></div>
</template>

<script>
function convert_progress_message() {
  //x[0] is starttime
}
export default {
  mounted() {
    var plot_data = [
      {
        type: "sankey",
        orientation: "h",
        node: {
          pad: 15,
          thickness: 30,
          line: {
            color: "black",
            width: 0.5,
          },
          label: ["A1", "A2", "B1", "B2", "C1", "C2"],
          color: ["blue", "blue", "blue", "blue", "blue", "blue"],
        },

        link: {
          source: [0, 1, 0, 2, 3, 3],
          target: [2, 3, 3, 4, 4, 5],
          value: [8, 4, 2, 8, 4, 2],
        },
      },
      {
        type: "sankey",
        orientation: "h",
        node: {
          pad: 15,
          thickness: 30,
          line: {
            color: "blue",
            width: 0.5,
          },
          label: ["A3", "A4", "B4", "B2", "C1", "C2"],
          color: ["blue", "blue", "blue", "blue", "blue", "blue"],
        },

        link: {
          source: [4, 5, 4, 4, 5, 4],
          target: [2, 3, 3, 4, 4, 5],
          value: [8, 4, 2, 8, 4, 2],
        },
      },
    ];
    var plot_layout = {
      title: "Testgraph",
      height: 300,
      yaxis: {
        showgrid: false,
        zeroline: false,
        showline: false,
        showticklabels: false,
      },
    };
    var plot_config = {
      responsive: true,
    };
    this.$plotly.newPlot("progresgraph", plot_data, plot_layout, plot_config);
  },
  methods: {
    connectToProjectSocketIoRoom() {
      this.$socket.emit("join_project_updates", {
        project_id: this.project.id,
        access_token: this.$store.state.login.jwt,
      });
      this.$socket.on("new-workflow-log", (new_log) => {
        console.log("New log:");
        console.log(new_log);
      });
      this.$socket.on("finished-project", () => {
        console.log("Finished project");
      });
      this.$socket.on("new-progress", (data) => {
        console.log("New Progress:");
        console.log(data);
      });
    },
    disconnectFromProjectSocketIoRoom() {
      if (this.project != null)
        this.$socket.emit("leave_project_updates", {
          project_id: this.project.id,
        });
    },
  },
};
</script>
