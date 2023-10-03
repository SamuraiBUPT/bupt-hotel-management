<template>
  <div style="margin: 20px"></div>
  <el-form
    :label-position="labelPosition"
    label-width="100px"
    :model="formLabelAlign"
    style="max-width: 460px">

    <el-form-item label="Username">
      <el-input v-model="formLabelAlign.username" type="text"
      placeholder="Please Input username"/>
    </el-form-item>

    <el-form-item label="Password">
      <el-input v-model="formLabelAlign.password" type="password" placeholder="Please Input password"/>
    </el-form-item>

    <el-form-item label="Verify">
      <el-input v-model="formLabelAlign.verify_code" style="width: 40%" type="text"/>
    </el-form-item>

    <el-form-item>
      <div style="width: 75%"></div>
      <el-button type="primary" @click="onSubmit">Login</el-button>
    </el-form-item>
  </el-form>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'

const labelPosition = ref('right')

const formLabelAlign = reactive({
  username: '',
  password: '',
  verify_code: '',
})

const onSubmit = () => {
  console.log('submit!')
}
</script>

<style scoped>

</style>