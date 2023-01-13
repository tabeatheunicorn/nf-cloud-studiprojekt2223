<template>
  <div>
    <p>
      Running since:
      {{ elapsedTime }}s
    </p>
  </div>
</template>

<script>
export default {
  name: "TimerComponent",
  data() {
    return {
      startTime: null,
      elapsedTime: null,
    };
  },
  created() {
    this.startTime = Date.now();
    setInterval(() => {
      this.elapsedTime = Math.floor((Date.now() - this.startTime) / 1000);
    }, 1000);
  },
};
</script>
