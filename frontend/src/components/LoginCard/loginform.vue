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
      <div style="display: flex">
        <el-input v-model="formLabelAlign.verify_code" style="width: 100px" type="text"/>
      </div>
      <div style="flex: 1; margin-left: 30px">
        <ValidCode style="height: 32px; width: 90px" @update:value="getCode" ref="ValidCodeRef"/>
      </div>
    </el-form-item>

    <el-form-item>
      <div style="width: 75%"></div>
      <el-button type="primary" @click="onSubmit">Login</el-button>
    </el-form-item>
  </el-form>
</template>

<script>
import ValidCode from '../ValidCode/validcode.vue';
import api from '../../api';
import { ElMessage } from 'element-plus';
import {h} from 'vue';

export default {
  name: 'LoginForm',
  components: {
    ValidCode
  },
  data() {
    return {
      labelPosition: 'right',
      formLabelAlign: {
        username: '',
        password: '',
        verify_code: '',
      },
      code_value: ''
    }
  },
  methods: {
    onSubmit() {
      console.log('validating...');
      // first validate the verify code
      const code_submit = this.formLabelAlign.verify_code.toLowerCase();
      const code_valid = this.code_value.toLowerCase();
      if (code_submit != code_valid) {
        console.log('verify code error');
        alert("验证码错误，请重新输入！");
        this.$refs.ValidCodeRef.refreshCode();
        return;
      }
      else {
        // api.postLogin(this.formLabelAlign);
        api.postLogin({
          account: this.formLabelAlign.username,
          password: this.formLabelAlign.password
        }).then(res => {
          console.log(res);
          if (res.status == 200) {
            console.log('login success');
            console.log(res.data.identity)
            let identity = res.data.identity; // str
            let role = null;
            if (identity == '0') {
              // admin: 空调管理员
              role = 'admin';
            }
            else if (identity == '1') {
              // reception: 前台
              role = 'reception';
            }
            else if (identity == '2') {
              // manager: 酒店经理
              role = 'manager';
            }
            this.$store.commit('setLogin', role);
            this.redirectUser(role);
          }
          else {
            console.log('login failed');
            ElMessage.error("用户名或密码错误！");
            this.$refs.ValidCodeRef.refreshCode();
            return;
          }
        }).catch(err => {
          console.log(err);
        });
      }
    },
    getCode(code) {
      // console.log(code);
      this.code_value = code;
    },
    redirectUser(role) {
      if(role == 'admin') {
        this.$router.push('/ac');
      }
      else if(role == 'reception') {
        this.$router.push('/reception');
      }
      else if(role == 'manager') {
        this.$router.push('/manager');
      }
      this.$router.push(redirect);
    }
  }
}
</script>

<style scoped>

</style>