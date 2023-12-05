<template>
  <el-card @click="OfferDetail" @mouseover="handleMouseOver" @mouseout="handleMouseOut"
  :class="{hovered: isHovered, 'green-bg': state === 'empty', 'gray-bg': state !== 'empty'}" 
  style="width: 200px; height: 150px;">
    <div class="text item" style="padding: 5px;">Room ID: {{ room_id }}</div>
    <div class="text item" style="padding: 5px;">Cost: {{ cost }}</div>
    <div class="text item" style="padding: 5px;">state: {{ state }}</div>
  </el-card>

    <!-- 对话框 -->
  <el-dialog
    v-model="dialogVisible"
    title="详情"
    width="55%"
  >
    <div v-if="state !== 'empty'" style="max-height: 400px; overflow-y: auto;">
      <table>
        <!-- 表头 -->
        <tr>
          <th style="width: 80px">序号</th>
          <th style="width: 80px">房间号</th>
          <th style="width: 200px">请求时间</th>
          <th style="width: 200px">服务开始时间</th>
          <th style="width: 200px">服务结束时间</th>
          <th style="width: 100px">服务时长</th>
          <th style="width: 80px">风速</th>
          <th style="width: 100px">当前费用</th>
          <th style="width: 80px">费率</th>
        </tr>
        <tr v-for="record in records" :key="record.id">
          <td style="width: 80px; text-align: center;">{{ record.id }}</td>
          <td style="width: 80px; text-align: center;">{{record.room_id}}</td>
          <td style="width: 200px; text-align: center;">{{record.req_date_time}}</td>
          <td style="width: 200px; text-align: center;">{{record.serve_start_time}}</td>
          <td style="width: 200px; text-align: center;">{{record.serve_end_time}}</td>
          <td style="width: 100px; text-align: center;">{{record.serve_time}}</td>
          <td style="width: 80px; text-align: center;">{{record.wind}}</td>
          <td style="width: 100px; text-align: center;">{{record.current_bill}}</td>
          <td style="width: 80px; text-align: center;">{{record.rate}}</td>
        </tr>
      </table>
    </div>

    <!-- 结账 -->
    <template #footer>
      <span class="dialog-footer">
        <el-button type="primary" @click="checkout">
          {{ state === 'empty' ? '入住' : '结账' }}
        </el-button>
        <el-button @click="dialogVisible = false">关闭</el-button>
      </span>
    </template>
  </el-dialog>


</template>

<script>
import { ElMessageBox } from 'element-plus';
export default {
  props: {
    room_id: Number,
    cost: Number,
    state: String,
    role: String,
  },
  data() {
    return {
      isHovered: false,
      dialogVisible: false,
      records: [],
    }
  },
  methods: {
    OfferDetail() {
      this.dialogVisible = true;
      console.log("OfferDetail");

      this.records = [
        { 
          id: 1, room_id: this.room_id, 
          req_date_time: '2023-01-01 13:26:24', serve_start_time: '2023-01-01 13:27:24', 
          serve_end_time: '2023-01-01 18:27:24', 
          serve_time: '16.5',
          wind: 'Low', current_bill: '100.1', rate: '1.0' 
        },
        { 
          id: 2, room_id: this.room_id, 
          req_date_time: '2023-01-01 13:26:24', serve_start_time: '2023-01-01 13:26:24', 
          serve_end_time: '2023-01-01 13:26:24', 
          serve_time: '27.8',
          wind: 'Low', current_bill: '100.1', rate: '1.0' 
        },
        // ... 更多记录 ...
      ];
    },

    handleMouseOver() {
      this.isHovered = true;
      console.log("handleMouseOver");
    },
    handleMouseOut() {
      this.isHovered = false;
      console.log("handleMouseOut");
    },
    handleConfirm() {
      // 确认按钮的处理逻辑
      console.log('确认操作');
      this.dialogVisible = false; // 关闭对话框
    },
    checkout() {
      // 结账按钮的处理逻辑
      // ...
    }
  }
}

</script>

<style scoped>
/* 基本样式 */
.el-card {
  transition: border 0.3s; /* 平滑的过渡效果 */
}

/* 悬停效果 */
.el-card.hovered {
  border: 1px solid rgb(29, 168, 215);
  cursor: pointer;
}
.el-card.green-bg {  
  background-color: #C8E6C9;   
}  
  
.el-card.gray-bg {  
  background-color: #d3d3d3;  
}


</style>





