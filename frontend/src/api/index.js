import axios from "../utils/requests_wrapper.js"
import path from "./path.js"

const api = {
  getChengpin(){
    return axios.get(path.baseUrl + path.chengpin);
  },
  getData(){
    return axios.get(path.localTEST);
  },
  postLogin(data){
    return axios.post(path.login, data);
  }
}

export default api;