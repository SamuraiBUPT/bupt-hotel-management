<template>  
  <el-container>  
    <el-aside>  
      <MenuRight class="menu" />  
    </el-aside>  
    <el-container style="display: flex; flex-wrap: wrap;">  
      <div  
        v-for="(room, index) in rooms"  
        :key="index"  
        style="width: 200px; margin: 6px; padding: 0;"  
      >  
        <RoomGrid :room_id="room.id" :cost="room.cost" style="margin: 0; padding: 0;" />  
      </div>  
    </el-container>  
  </el-container>  
</template>

<script>
import MenuRight from '../../components/MenuRight/menuright.vue'
import RoomGrid from '../../components/RoomGrid/roomgrid.vue'
export default {
  name: 'PanelView',
  data() {
    return {
      rooms: [  
        { id: 1, cost: 50 },  
        { id: 2, cost: 60 },  
        { id: 251, cost: 70 },  
        { id: 249, cost: 50 },  
        { id: 250, cost: 60 },  
        { id: 251, cost: 70 },
        { id: 249, cost: 50 },  
        { id: 250, cost: 60 },  
        { id: 251, cost: 70 },
        { id: 249, cost: 50 },  
        { id: 250, cost: 60 },  
        { id: 251, cost: 70 },
        { id: 249, cost: 50 },  
        { id: 250, cost: 60 },  
        { id: 251, cost: 70 },
        { id: 249, cost: 50 },  
        { id: 250, cost: 60 },  
        { id: 251, cost: 70 },
        { id: 249, cost: 50 },  
        { id: 250, cost: 60 },  
        { id: 251, cost: 70 },
        { id: 1, cost: 50 },  
        { id: 2, cost: 60 },  
        { id: 251, cost: 70 },  
        { id: 249, cost: 50 },  
        { id: 250, cost: 60 },  
        { id: 251, cost: 70 },
        { id: 249, cost: 50 },  
        { id: 250, cost: 60 },  
        { id: 251, cost: 70 },
        { id: 249, cost: 50 },  
        { id: 250, cost: 60 },  
        { id: 251, cost: 70 },
        { id: 249, cost: 50 },  
        { id: 250, cost: 60 },  
        { id: 251, cost: 70 },
        { id: 249, cost: 50 },  
        { id: 250, cost: 60 },  
        { id: 251, cost: 70 },
        { id: 249, cost: 50 },  
        { id: 250, cost: 60 },  
        { id: 251, cost: 70 },
        // 这里需要用数据库捕获信息 
      ],  
    }
  },
  components: {
    MenuRight,
    RoomGrid,
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
