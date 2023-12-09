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
  },
  postCheckIn(data){
    return axios.post(path.checkIn, data);
  },
  postCheckOut(data){
    return axios.post(path.checkOut, data);
  },
  postTurnOn(data){
    return axios.post(path.turnOn, data);
    // return axios.post(path.turnOn + '/', data);
  },
  postTurnOff(data){
    return axios.post(path.turnOff, data);
    // return axios.post(path.turnOff + '/', data);
  },
  postSetTemperature(data){
    return axios.post(path.setTemperature, data);
    // return axios.post(path.setTemperature + '/', data);
  },
  postSetSpeed(data){
    return axios.post(path.setSpeed, data);
    // return axios.post(path.setSpeed + '/', data);
  },
  postSetTemperatureInit(data){
    return axios.post(path.setTemperatureInit, data);
  },
  getQueryRoomInfo(data){
    return axios.get(path.queryRoomInfo, {params: data});
  },
  postUpdateRooms(data){
    return axios.post(path.updateRooms, data);
  },
  getRoomList(){
    return axios.get(path.roomList);
  },
  getForm(){
    return axios.get(path.getForm);
  },
  postCurTemperature(data){
    return axios.post(path.send_cur_temp, data);
  },
  getDetail(data){
    return axios.get(path.detail, {params: data});
  },
  getBill(data){
    return axios.get(path.bill, {params: data});
  }
}

export default api;