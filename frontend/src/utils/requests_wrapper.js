import axios from 'axios'
import qs from 'qs'

function errorHandle(status, other) {
  switch (status) {
    case 400:
      console.log("信息校验失败");
      break;
    case 401:
      console.log("服务器认证失败");
      break;
    case 403:
      console.log("服务器拒绝访问");
      break;
    case 404:
      console.log("请求资源不存在");
      break;
    case 502:
      console.log("服务器错误");
      break;
    default:
      console.log(other);
      break;
  }
}

// const instance = axios.create({
//   timeout: 5000
// });

// 设置拦截器
axios.interceptors.request.use(
  config => {
    if (config.method === "post") {
      // let lidongyuan = true;
      let lidongyuan = false;
      if (lidongyuan) {
        config.url = config.url + '/';
      }
    }
    return config;
  },
  error => Promise.reject(error)
);

axios.interceptors.response.use(
  response => {
    return response.status === 200 ? Promise.resolve(response) : Promise.reject(response) // 这里会发送响应的失败信息
  },
  error => {  // 这里就是连发送请求都没成功
    const { response } = error;
    console.log(error);
    errorHandle(response.status, response.info);
  });

// axios.defaults.headers.post['Content-Type'] = 'text/html; charset=utf-8';

export default axios;