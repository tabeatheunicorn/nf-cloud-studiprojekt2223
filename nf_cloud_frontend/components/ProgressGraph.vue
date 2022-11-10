<template>
  <Plotly :data="data" :layout="layout"></Plotly>
</template>

<script>
import { plotly } from "~/components/Plotly";

export default {
  components: {
    plotly,
  },
  data() {
    return {
      data: [
        {
          type: "treemap",
          labels: [
            "Eve",
            "Cain",
            "Seth",
            "Enos",
            "Noam",
            "Abel",
            "Awan",
            "Enoch",
            "Azura",
          ],
          parents: ["", "Eve", "Eve", "Seth", "Seth", "Eve", "Eve", "Awan", "Eve"],
        },
      ],
      layout: {
        title: "My graph",
      },
    };
  },
};
</script>
