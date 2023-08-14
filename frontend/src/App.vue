<template>
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
  <VideoUpload />
  <WatchVideoVue />
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import VideoUpload from './components/VideoUpload.vue'
import WatchVideoVue from './components/WatchVideo.vue'

export default {
  name: 'App',
  components: {
    // HelloWorld,
    VideoUpload,
    WatchVideoVue
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
