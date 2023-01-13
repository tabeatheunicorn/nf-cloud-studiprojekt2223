<template>
  <div>
    <p>
      Die verstrichene Zeit seit dem Erhalt der Nachricht beträgt:
      {{ elapsedTime }} Sekunden
    </p>
  </div>
</template>

<script>
export default {
  name: "TimerComponent",
  data() {
    return {
      startTime: null,
    };
  },
  computed: {
    elapsedTime() {
      return Math.floor((Date.now() - this.startTime) / 1000);
    },
  },
  created() {
    this.startTime = Date.now();
    setInterval(() => {}, 1000);
  },
};
</script>
