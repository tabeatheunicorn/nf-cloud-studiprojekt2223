<template>
  <div id="progresgraph"></div>
</template>

<script>
export default {
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
