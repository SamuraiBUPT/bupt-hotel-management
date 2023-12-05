<template>
  <el-menu
    default-active="1"
    class="el-menu-vertical-demo"
    :collapse="isCollapse"
    @open="handleOpen"
    @close="handleClose"
  >
    <!-- 前台面板 -->
    <el-menu-item index="1" @click="goToRoute('/reception')">
      <el-icon><icon-menu /></el-icon>
      <span slot="title">前台面板</span>
    </el-menu-item>

    <!-- 空调管理员面板 -->
    <el-menu-item index="2" @click="goToRoute('/ac')">
      <el-icon><setting /></el-icon>
      <span slot="title">空调管理员面板</span>
    </el-menu-item>

    <!-- 经理面板 -->
    <el-menu-item index="3" @click="goToRoute('/manager')">
      <el-icon><document /></el-icon>
      <span slot="title">经理面板</span>
    </el-menu-item>
  </el-menu>
</template>

<script>
import { ref } from 'vue'
import {
  Document,
  Menu as IconMenu,
  Location,
  Setting,
} from '@element-plus/icons-vue'
export default {
  name: 'PanelView',
  data() {
    return {
      isCollapse: false
    }
  },
  components: {
    Document,
    IconMenu,
    Location,
    Setting,
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath)
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath)
    },
    goToRoute(route) {
      this.$router.push(route);
    },
  }
}
</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 250px;
  min-height: 800px;
}
</style>
