<template>
  <div id="app" class="terminal">
    <router-view />
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
.terminal {
  background-color: #000;
  color: #0f0;
  font-family: 'Courier New', Courier, monospace;
  padding: 20px;
  min-height: 100vh;
}
</style>

