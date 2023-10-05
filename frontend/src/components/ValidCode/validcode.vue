<template>
  <div class="ValidCode disabled-select" style="width: 100%; height: 100%" @click="refreshCode">
    <span v-for="(item, index) in codeList" :key="index" :style="getStyle(item)">{{ item.code }}</span>
  </div>
</template>

<script>
export default {
  name: 'ValidCode',
  data() {
    return {
      length: 4,
      codeList: []
    }
  },
  mounted() {
    this.createCode();
  },
  methods: {
    refreshCode() {
      this.createCode();
    },
    createCode() {
      const len = this.length;
      let codeList = [];
      const chars = 'ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz23456789';
      const charsLen = chars.length;

      // generate
      for (let i = 0; i < len; i++){
        let rgb = [Math.round(Math.random() * 220), Math.round(Math.random() * 240), Math.round(Math.random() * 200)];
        codeList.push({
          code: chars.charAt(Math.floor(Math.random() * charsLen)),
          color: `rgb(${rgb})`,
          padding: `${Math.floor(Math.random() * 10)}px`,
          transform: `rotate(${Math.floor(Math.random() * 90) - Math.floor(Math.random() * 90)}deg)`
        })
      }

      // point
      this.codeList = codeList;

      // send data
      this.$emit('update:value', codeList.map(item => item.code).join(''));
    },
    getStyle(data) {
      return `color: ${data.color}; font-size: ${data.fontSize}; padding: ${data.padding}; transform: ${data.transform};}`
    }
  }
}
</script>

<style scoped>
.ValidCode {
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
}
.ValidCode span {
  display: inline-block;
  font-size: 18px;
}
</style>