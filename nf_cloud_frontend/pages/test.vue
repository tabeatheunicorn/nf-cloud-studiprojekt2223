<template>
<div id="div">
</div>
</template>

<script>
export default {
  head(){
        return {
            title: "Testpage",
            script: [
                {
                    hid: "plotly",
                    src: "https://cdn.plot.ly/plotly-2.16.1.min.js",
                    defer: true,
                    // callback: () => { this.isPlotlyLoaded = true }
                }
            ]
        }
    },

    
    components: {
    Plotly
  },

  data() {
    return {
      data:[{
        x: [1,2,3,4],
        y: [10,15,13,17],
        type:"scatter"
      }],
      layout:{
        title: "My graph"
      }
    }
  }
}
</script>