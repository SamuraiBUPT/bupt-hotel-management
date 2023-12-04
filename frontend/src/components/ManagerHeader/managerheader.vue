<template>
    <el-header style="background-color: lightblue;width: 100%;">
        <div class="text item" style="padding: 5px;">身份: {{ identity }}</div>
        <div class="text item" style="padding: 5px;">客房信息: {{ num }}/{{ total }}</div>
    </el-header>
</template>

<script>
export default {
  props: {
    identity: String,
    num: Number,
    total: Number,
  },
  data() {
    return {}
  },
}

</script>