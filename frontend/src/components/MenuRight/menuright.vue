<template>
  <el-menu
    default-active="activeIndex"
    class="el-menu-vertical-demo"
    :collapse="isCollapse"
    @open="handleOpen"
    @close="handleClose"
  >
    <!-- 前台面板 -->
    <el-menu-item index="1" @click="setActiveIndex('1', '/reception')">
      <el-icon><icon-menu /></el-icon>
      <span slot="title">前台面板</span>
    </el-menu-item>

    <!-- 空调管理员面板 -->
    <el-menu-item index="2" @click="setActiveIndex('2', '/ac')">
      <el-icon><setting /></el-icon>
      <span slot="title">空调管理员面板</span>
    </el-menu-item>

    <!-- 经理面板 -->
    <el-menu-item index="3" @click="setActiveIndex('3', '/manager')">
      <el-icon><document /></el-icon>
      <span slot="title">经理面板</span>
    </el-menu-item>

    <!-- 经理面板 -->
    <el-menu-item index="4" @click="setActiveIndex('4', '/client')">
      <el-icon><document /></el-icon>
      <span slot="title">客房空调面板</span>
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
      activeIndex: '1',
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
    setActiveIndex(idx, route) {
      this.activeIndex = idx;
      this.$router.push(route);
    }
  }
}
</script>

<style>
.el-menu-vertical-demo:not(.el-menu--collapse) {
  width: 250px;
  min-height: 800px;
}
</style>
