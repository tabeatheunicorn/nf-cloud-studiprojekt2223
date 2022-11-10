<template>
  <Plotly :data="data" :layout="layout"></Plotly>
</template>

<script>
import { Plotly } from "@rleys/vue-plotly-basic";

export default {
  components: {
    Plotly,
  },
  data() {
    return {
      data: [
        {
          x: [1, 2, 3, 4, 5, 6],
          y: [10, 15, 13, 17, 22, 3],
          type: "scatter",
        },
      ],
      layout: {
        title: "My graph",
      },
    };
  },
};
</script>
