<template>
<div class="container">
    <el-card class="box-card" style="height: 400px;">
    <!-- 第一行，高度较高的信息显示区，有边框 -->
    <div class="info-box" style="height: 150px">
        <!-- 根据开关状态显示不同的信息 -->
        <div v-if="!isPoweredOn">
            NULL
        </div>
        <div v-else>
            <!-- 第一行 -->
            <el-row class="info-row">
            <el-col :span="12">
                <div class="info-label">当前温度：</div>
                <div class="info-value">{{ currentTemperature }}</div>
            </el-col>
            <el-col :span="12">
                <div class="info-label">设定温度：</div>
                <div class="info-value">{{ setTemperature }}</div>
            </el-col>
            </el-row>

            <!-- 第二行 -->
            <el-row class="info-row">
            <el-col :span="12">
                <div class="info-label">当前风速：</div>
                <div class="info-value">{{ currentWindSpeed }}</div>
            </el-col>
            <el-col :span="12">
                <div class="info-label">设定风速：</div>
                <div class="info-value">{{ setWindSpeed }}</div>
            </el-col>
            </el-row>

            <!-- 第三行 -->
            <el-row class="info-row">
            <el-col :span="24">
                <div class="info-label">空调费用：</div>
                <div class="info-value">{{ airConditioningCost }}</div>
            </el-col>
            </el-row>
        </div>
    </div>

    <!-- 第二行，一个开机/关机按钮 -->
    <div class="row">
        <el-form ref="form1" :model="form1" inline>
            <el-form-item label="房间号">
                <el-input v-model="form1.field1" style="width: 200px;"></el-input>
            </el-form-item>
            <el-form-item>
                <el-button :class="buttonClass" @click="togglePower">{{ powerButtonLabel }}</el-button>
            </el-form-item>
        </el-form>
        <!-- <el-button :class="buttonClass" @click="togglePower">{{ powerButtonLabel }}</el-button> -->
    </div>

    <!-- 第三、四行，表单和按钮 -->
    <!-- 第三行，一个短输入栏和提交按钮 -->
    <div class="row">
    <el-form ref="form2" :model="form2" inline>
        <el-form-item label="设置温度">
            <el-input v-model="form2.field2" style="width: 200px;"></el-input>
        </el-form-item>
        <el-form-item>
            <el-button type="primary" @click="submitForm('form2')">SET</el-button>
        </el-form-item>
    </el-form>
    </div>

    <div class="row">
        <el-form ref="form3" :model="form3" inline>
            <el-form-item label="设置风速">
                <el-select v-model="form3.field3" placeholder="请选择" style="width: 200px;">
                <el-option label="Low" value="Low"></el-option>
                <el-option label="Medium" value="Medium"></el-option>
                <el-option label="High" value="High"></el-option>
                </el-select>
            </el-form-item>
            <el-form-item>
                <el-button type="primary" @click="submitForm('form3')">SET</el-button>
            </el-form-item>
        </el-form>
    </div>
    </el-card>
</div>
</template>

<script>
import api from '../../api';
export default {
data() {
    return {
        form1: {
            field1: ''
        },
        form2: {
            field2: ''
        },
        form3: {
            field3: ''
        },

        // 开关机按钮的状态
        isPoweredOn: false,
        currentTemperature: null,
        setTemperature: null,
        currentWindSpeed: null,
        setWindSpeed: null,
        airConditioningCost: null,
    };
},
computed: {
    // 计算属性，用于动态更新按钮文本
    buttonClass() {
        return this.isPoweredOn ? 'button-on' : 'button-off';
    },
    powerButtonLabel() {
        return this.isPoweredOn ? '关机' : '开机';
    }
},
created() {
    
},
beforeDestroy() {
    // 组件销毁时清理定时器
    if (this.intervalId) {
        clearInterval(this.intervalId);
    }
},
methods: {
    togglePower() {
        // 切换开关机状态
        this.isPoweredOn = !this.isPoweredOn;
        console.log(this.isPoweredOn ? "开机" : "关机");
        // 如果开机，则请求空调信息
        if (this.isPoweredOn) {
            this.intervalId = setInterval(this.fetchRoomInfo, 5000);
            // this.intervalId2 = setInterval(this.send_cur_temperature, 5000);
            this.fetchAirConditioningInfo();
        }
        else {
            this.turnOFF();
        }
        this.initialTime = new Date();
        this.currentTime = new Date();
        const room1_init = 32;
        const room2_init = 28;
        const room3_init = 30;
        const room4_init = 29;
        const room5_init = 31;
        const temp_init_dict = {
            "101": room1_init,
            "102": room2_init,
            "103": room3_init,
            "104": room4_init,
            "105": room5_init
        };
        this.currTemp = temp_init_dict[this.form1.field1];
        console.log("当前温度：", this.currTemp)

        // 每秒更新当前时间并重新计算温度
        this.timer = setInterval(() => {
            this.currentTime = new Date();
            this.calculateTemperature();
        }, 10000);
    },
    calculateTemperature() {
        // const minutesPassed = (this.currentTime - this.initialTime) / 10000; // 计算经过的分钟数
        
        if (this.currTemp == this.setTemperature) {
            return;
        }
        else if (this.currTemp > this.setTemperature) {
            this.currTemp -= 0.5 ;
        }
        else {
            this.currTemp += 0.5 ;
        }
        console.log("当前温度：", this.currTemp)
        console.log("发送请求")
        // this.send_cur_temperature();
    },
    fetchRoomInfo(){
        api.getQueryRoomInfo({
            room_number: this.form1.field1
        }).then(res => {
            console.log("res:", res);
            // 更新数据
            // this.currentTemperature = res.data.cur_temperature;
            this.currentTemperature = this.currTemp;
            this.setTemperature = res.data.set_temperature;
            this.currentWindSpeed = res.data.speed;
            this.setWindSpeed = res.data.speed;
            this.airConditioningCost = res.data.bill;
        }).catch(err => {
            console.error('Error fetching room info:', err);
            alert("error！");
        });
    },
    send_cur_temperature() {
        console.log("发送出去的温度：", this.currTemp)
        api.postCurTemperature({
            room_number: this.form1.field1, current_temp: this.currTemp
        }).catch(err => {
            console.log(err);
            console.log('send failed');
            alert("请检查房间号是否正确！");
        });
    },
    fetchAirConditioningInfo() {
        // 这里是请求后端获取空调信息的逻辑
        // 假设您从后端获取的信息是一个对象，例如：
        // { currentTemperature: 24, setTemperature: 26, currentWindSpeed: 3, setWindSpeed: 2, airConditioningCost: 100 }
        // 您需要根据实际情况调整这个方法来适应您的后端接口

        // 模拟异步请求获取数据
        this.fetchRoomInfo();
        
        // 在这里，我们首先的逻辑是向后端告知我们打开了空调，然后后端返回给我们一个对象，包含了空调的信息
        this.submitForm('form1');
    },
    submitForm(form_name) {
        if(form_name === "form1") {
            api.postTurnOn({
                room_number: this.form1.field1
            }).then(res => {
                console.log(res);
                if (res) {
                    console.log('turn on success');
                    console.log(res.data);
                }
            }).catch(err => {
                console.log(err);
                console.log('turn on failed');
                alert("开机失败，请检查房间号是否正确！");
            });
        } else if (form_name === "form2") {
            api.postSetTemperature({
                room_number: this.form1.field1, temperature: parseInt(this.form2.field2)
            }).catch(err =>{
                console.log(err);
                console.log('set failed');
                alert("请检查房间号是否正确！");
            });
        } else if (form_name === "form3") {
            let speed_ = this.form3.field3;
            // 转换为小写
            speed_ = speed_.toLowerCase();
            api.postSetSpeed({
                room_number: this.form1.field1, speed: speed_
            }).catch(err =>{
                console.log(err);
                console.log('set failed');
                alert("请检查房间号是否正确！");
            });
        }
    },
    turnOFF() {
        api.postTurnOff({
            room_number: this.form1.field1
        }).then(res => {
            console.log(res);
            if (res) {
                console.log('turn off success');
                console.log(res.data);
            }
        }).catch(err => {
            console.log(err);
            console.log('turn off failed');
            alert("关机失败，请检查房间号是否正确！");
        });
    }
}
};
</script>

<style scoped>
.container {
display: flex;
justify-content: center; /* 水平居中 */
align-items: center; /* 垂直居中 */
height: 100vh; /* 全视口高度 */
}

.box-card {
width: 33%; /* 卡片宽度设置为页面的三分之一 */
}

.info-box {
border: 1px solid #dcdfe6; /* 信息区边框 */
padding: 10px;
margin-bottom: 20px;
flex-direction: column;
}

.row {
margin-bottom: 20px;
}

/* 添加自定义样式 */
.button-on {
    background-color: #f85050;
}
.button-off {
  /* 默认样式，可以根据需要进行调整 */
}

.info-row {
  margin-bottom: 10px; /* 行间距 */
}

.info-label, .info-value {
  display: inline-block; /* 内联块布局 */
}

.info-label {
  margin-right: 10px; /* 标签后的间隔 */
}
</style>
