<template>
  <el-card @click="OfferDetail" @mouseover="handleMouseOver" @mouseout="handleMouseOut"
  :class="{hovered: isHovered}">
    <div class="text item">Room ID: {{ room_id }}</div>
    <div class="text item">Cost: {{ cost }}</div>
  </el-card>
</template>

<script>
export default {
  props: {
    room_id: Number,
    cost: Number
  },
  data() {
    return {
      isHovered: false
    }
  },
  methods: {
    OfferDetail() {
      console.log("OfferDetail");
    },
    handleMouseOver() {
      this.isHovered = true;
      console.log("handleMouseOver");
    },
    handleMouseOut() {
      this.isHovered = false;
      console.log("handleMouseOut");
    }
  }
}

</script>

<style scoped>
/* 基本样式 */
.el-card {
  transition: border 0.3s; /* 平滑的过渡效果 */
}

/* 悬停效果 */
.el-card.hovered {
  border: 1px solid rgb(29, 168, 215);
  cursor: pointer;
}

/* 可以根据需要添加其他样式 */
</style>





