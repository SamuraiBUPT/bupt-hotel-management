<template>
  <div class="container">
    <MenuRight class="menu"/>
    <RoomGrid 
    :room_id="249"
    :cost="50"/>

  </div>
</template>

<script>
import MenuRight from '../../components/MenuRight/menuright.vue'
import RoomGrid from '../../components/RoomGrid/roomgrid.vue'
export default {
  name: 'PanelView',
  data() {
    return {
      
    }
  },
  components: {
    MenuRight,
    RoomGrid
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
