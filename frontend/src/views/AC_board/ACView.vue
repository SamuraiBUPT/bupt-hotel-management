<template>  
    <el-container style="overflow: hidden;">  
      <el-aside style="height: 100%; width: 20%">  
        <MenuRight class="menu"/>  
      </el-aside>  
      <el-container style="display: flex; flex-wrap: wrap; height: 100%; width: 80%; overflow: hidden;">  
        <ManagerHeader :identity="identity.identity" :num="identity.num" :total="identity.total" class="managerheader" style=" height: 10%"/>
        <el-container style="display: flex; flex-wrap: wrap; width: 800px; height: 750px; overflow: scroll;"> 
          <div  
            v-for="(room, index) in rooms"  
            :key="index"  
            style="width: 200px; margin: 6px; padding: 0;"  
          >  
            <ACGrid :room_id="room.id" :state="room.state" style="margin: 0; padding: 0;" />  
          </div>  
        </el-container>
      </el-container>  
    </el-container>  
  </template>
  
  <script>
  import MenuRight from '../../components/MenuRight/menuright.vue'
  import ACGrid from '../../components/ACGrid/acgrid.vue'
  import ManagerHeader from '../../components/ManagerHeader/managerheader.vue'
  export default {
    name: 'PanelView',
    data() {
      return {
        identity: {identity:"空调管理员", total: 36, num: 34},
        rooms: [  
          { id: 1, cost: 50, state: "error" },  
          { id: 2, cost: 60, state: "error"  },  
          { id: 251, cost: 70, state: "error" },  
          { id: 249, cost: 50, state: "error" },  
          { id: 250, cost: 60, state: "working" },  
          { id: 251, cost: 70, state: "working" },
          { id: 249, cost: 50, state: "working" },  
          { id: 250, cost: 60, state: "working" },  
          { id: 251, cost: 70, state: " " },  
          { id: 249, cost: 50, state: " " },  
          { id: 250, cost: 60, state: " " },  
          { id: 251, cost: 70, state: " " },
          { id: 249, cost: 50, state: " " },  
          { id: 250, cost: 60, state: " " },  
          { id: 251, cost: 70, state: " " },  
          { id: 249, cost: 50, state: " " },  
          { id: 250, cost: 60, state: " " },  
          { id: 251, cost: 70, state: " " },
          { id: 249, cost: 50, state: " " },  
          { id: 250, cost: 60, state: " " },  
          { id: 251, cost: 70, state: " " },  
          { id: 249, cost: 50, state: " " },  
          { id: 250, cost: 60, state: " " },  
          { id: 251, cost: 70, state: " " },
          { id: 249, cost: 50, state: " " },  
          { id: 250, cost: 60, state: " " },  
          { id: 251, cost: 70, state: " " },  
          { id: 249, cost: 50, state: " " },  
          { id: 250, cost: 60, state: " " },  
          { id: 251, cost: 70, state: " " },
          { id: 249, cost: 50, state: " " },  
          { id: 250, cost: 60, state: " " },  
          { id: 251, cost: 70, state: " " },  
          { id: 249, cost: 50, state: " " },  
          { id: 250, cost: 60, state: " " },  
          { id: 251, cost: 70, state: " " },
          { id: 249, cost: 50, state: " " },  
          { id: 250, cost: 60, state: " " },  
          // 这里需要用数据库捕获信息 
        ],  
      }
    },
    components: {
      ManagerHeader,
      MenuRight,
      ACGrid,
    },
    methods: {
      
    }
  }
  </script>
  
  <style>
  .container {
    display: flex;
    flex-direction: row;
    height: 100vh;
  }
  .menu {
    height: 100%
  }
  .content {
    flex: 1;  /* 使 RoomGrid 填充容器的剩余空间 */
  }
  
  </style>