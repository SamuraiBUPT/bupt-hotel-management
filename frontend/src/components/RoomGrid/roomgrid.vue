<template>
  <el-card @click="OfferDetail" @mouseover="handleMouseOver" @mouseout="handleMouseOut"
  :class="{hovered: isHovered, 'green-bg': state === 'empty', 'gray-bg': state !== 'empty'}" 
  style="width: 200px; height: 150px;">
    <div class="text item" style="padding: 5px;">Room ID: {{ room_id }}</div>
    <div class="text item" style="padding: 5px;">Cost: {{ cost }}</div>
    <div class="text item" style="padding: 5px;">state: {{ state }}</div>
  </el-card>
</template>

<script>
import { ElMessageBox } from 'element-plus';
export default {
  props: {
    room_id: Number,
    cost: Number,
    state: String,
  },
  data() {
    return {
      isHovered: false
    }
  },
  methods: {
    OfferDetail() {
      console.log("OfferDetail");

      const records = [
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

      const tableHtml = `
        <table style="width: 100%;">
          <tr>
            <th>序号</th>
            <th>房间号</th>
            <th>请求时间</th>
            <th>服务开始时间</th>
            <th>服务结束时间</th>
            <th>服务时长</th>
            <th>风速</th>
            <th>当前费用</th>
            <th>费率</th>
          </tr>
          ${records.map(record => `
            <tr>
              <td>${record.id}</td>
              <td>${record.room_id}</td>
              <td>${record.req_date_time}</td>
              <td>${record.serve_start_time}</td>
              <td>${record.serve_end_time}</td>
              <td>${record.serve_time}</td>
              <td>${record.wind}</td>
              <td>${record.current_bill}</td>
              <td>${record.rate}</td>
            </tr>
          `).join('')}
        </table>
      `;

      ElMessageBox({
        title: '详单',
        message: tableHtml,
        dangerouslyUseHTMLString: true,  // 允许使用 HTML 字符串
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        customClass: 'custom-message-box', // 添加自定义类名
        customStyle: {                    // 添加自定义内联样式
          width: '80%',                   // 增加消息框的宽度
          // maxHeight: '600px',              // 设置最大高度
          maxWidth: '900px',               // 设置最大宽度
        },
      });
      
    },
    handleMouseOver() {
      this.isHovered = true;
      console.log("handleMouseOver");
    },
    handleMouseOut() {
      this.isHovered = false;
      console.log("handleMouseOut");
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

/* 可以根据需要添加其他样式 */
.custom-message-box .el-message-box__content {
  overflow: auto; /* 超出内容时显示滚动条 */
}

.custom-message-box .el-message-box__content table {
  width: 100%; /* 表格宽度占满容器 */
}

.custom-message-box th, .custom-message-box td {
  border: 1px solid #040101; /* 单元格边框 */
  padding: 15px; /* 单元格内边距 */
  text-align: center; /* 文本左对齐 */
  min-width: 200px; /* 设置单元格的最小宽度 */
}
</style>





