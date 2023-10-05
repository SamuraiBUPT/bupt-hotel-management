<template>
  <el-card shadow="always" style="width: 800px;">
    <el-row>
      <el-col :span="12">
        <div style="margin-top: 65px"></div>
        <div>
          <img src="../../assets/photos/bupt-words.jpg" style="width: 350px;">
        </div>
      </el-col>
      <el-col :span="12">
        <div style="margin-top: 50px"></div>
        <LoginForm />
      </el-col>
    </el-row>
  </el-card>
  
</template>

<script setup>
import LoginForm from "./loginform.vue";


</script>

<style scoped>

</style>