<template>
  <table>
    <thead>
      <tr>
        <th v-for="key in Object.keys(items[0])" :key="key">{{ key }}</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="item in items" :key="item.id">
        <td v-for="key in Object.keys(item)">{{ item[key] }}</td>
      </tr>
    </tbody>
  </table>
</template>

<script>
export default {
  name: "WeblogMessageTable",
  props: {
    items: {
      type: Array,
      required: true,
    },
  },
};
</script>
