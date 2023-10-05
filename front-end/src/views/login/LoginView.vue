<template>
  <div id="loginbackground">
    <LoginCard />
  </div>
</template>

<script>
  import LoginCard from "../../components/LoginCard/logincard.vue"
  export default {
    name: 'LoginView',
    components: {
      LoginCard
    }
  }
</script>

<style>
body, html {
  margin: 0;
  height: 100%;
  font-family: 'Arial', sans-serif;
  background-image: url('../../assets/photos/loginbg2_jpg.jpg');
  background-size: cover;
  background-position: center;
  overflow: hidden;
}

/* 这是一个全屏的容器，用于放置背景和 LoginCard */
#loginbackground {
  display: flex;
  justify-content: center; /* 水平居中 */
  align-items: center;     /* 垂直居中 */
  width: 100vw;  /* 视窗的宽度 */
  height: 100vh; /* 视窗的高度 */
  position: relative; /* 为了确保::before 伪元素正确定位 */
  opacity: 0.9;
}

/* 添加蒙版效果，使背景图像模糊 */
body::before {
  content: "";
  position: fixed; /* 使用fixed，确保伪元素始终覆盖整个页面 */
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(255, 255, 255, 0.1); 
  backdrop-filter: blur(1px);
  z-index: 0;
}
</style>
