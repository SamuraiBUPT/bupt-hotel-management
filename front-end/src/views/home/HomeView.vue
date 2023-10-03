<template>
  <div>
    <h1>Home</h1>
    <button @click="pullReq">Click me</button>
    <button @click="testLocal">LocalAPI</button>
  </div>
</template>

<script>
import api from '../../api'
export default {
  data() {
    return {
      msg: "welcome to Home"
    }
  },
  methods: {
    pullReq() {
      api.getChengpin();
    },
    testLocal() {
      api.getData();
    }
  }
}
</script>