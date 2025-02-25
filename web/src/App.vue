<template>
  <div id="app">
    <ImageCompare />
  </div>
</template>

<script>
import ImageCompare from './components/ImageCompare.vue'

export default {
  name: 'App',
  components: {
    ImageCompare
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
